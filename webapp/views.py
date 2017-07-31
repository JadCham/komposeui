from django.shortcuts import render
from webapp.kompose.KomposeExceptions.KomposeConvertException import KomposeConvertException
from webapp.kompose.KomposeFileManager import KomposeFileManager
from webapp.kompose.KomposeWrapper import kompose_convert_web, kompose_convert_multiple_files
from .forms import UploadFileForm
from .models import Upload
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
import json


def get_client_ip(request):
    """"
    :params request: Django request
    Returns client ip address in xxx.xxx.xxx.xxx format
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def convert(upload):

    # Generate Kubernetes file
    to_convert = ""
    if upload.input_text:
        to_convert = upload.input_text
    elif upload.input_file:
        to_convert = upload.input_file.read().decode("utf-8")
    kompose_file_manager = KomposeFileManager()
    error = ""
    try:
        docker_compose_file_path = kompose_file_manager.write_yaml_to_file(to_convert)
        warning, kubernetes_yaml = kompose_convert_web(docker_compose_file_path, kompose_file_manager)
        upload.output_text = kubernetes_yaml
        upload.warning = warning
        upload.save()
        kompose_file_manager.cleanup_docker_compose_path(docker_compose_file_path)
        success = True
    except KomposeConvertException as e:
        error = str(e)
        kompose_file_manager.cleanup_docker_compose_path(docker_compose_file_path)
        success = False
    except Exception as e:
        error = "Something Went Wrong :("
        success = False
    return success, error


def download_yaml_zip(upload):

    # Generate Kubernetes file
    to_convert = ""
    if upload.input_text:
        to_convert = upload.input_text
    elif upload.input_file:
        to_convert = upload.input_file.read().decode("utf-8")

    kompose_file_manager = KomposeFileManager()
    error = ""

    try:
        folder_path = kompose_file_manager.get_folder_path(to_convert)
        kompose_convert_multiple_files(folder_path, kompose_file_manager)
        zip_path = kompose_file_manager.get_zip_file_path()
        kompose_file_manager.cleanup_yaml_folder_path()
        upload.output_file = zip_path
        success = True
    except KomposeConvertException as e:
        kompose_file_manager.cleanup_yaml_folder_path()
        error = str(e)
        success = False
    except Exception as e:
        kompose_file_manager.cleanup_yaml_folder_path()
        error = str(e)
        success = False

    upload.save()
    return success, error


def index(request):
    if request.method == 'POST':    # Check for POST method
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():     # Check if form is valid
            data_input = form.cleaned_data.get("input_text")
            data_file = form.cleaned_data["input_file"]
            upload = Upload(ip=get_client_ip(request), timestamp=timezone.now())

            # Check for uploaded text
            if data_input and len(data_input) > 0:
                upload.input_text = data_input
            # Check for uploaded file
            if data_file and len(data_file) > 0:
                upload.input_file = data_file

            if upload.input_text or upload.input_file:
                if form.cleaned_data["file_upload"]:
                    conversion = download_yaml_zip(upload)  # kompose conversion function with file
                else:
                    conversion = convert(upload)  # kompose conversion function no file
                # Check for conversion success
                if conversion[0]:
                    serialized = serializers.serialize("json", [upload])
                    serialized = json.dumps(json.loads(serialized)[0])  # Serialize output model
                    if upload.input_file:

                        # Send success message and output Model with input file
                        return JsonResponse({"success": True, "status": "Object Converted", "data": serialized,
                                             "input_file": upload.input_file.read().decode("utf-8")})

                        # Send success message and output Model without file
                    return JsonResponse({"success": True, "status": "Object Converted", "data": serialized})

                # Send conversion error message
                return JsonResponse({"status": "An Error Occurred in the conversion<br>"+conversion[1], "success": False})

            # Send empty upload error (empty file and text)
            return JsonResponse({"status": "Please fill in the input or upload a file", "success": False})

        # Sending form not valid error
        return JsonResponse({"status": "Please try again!", "success": False})

    # Rendering template page and form for GET request
    return render(request, 'base.html', {'form': UploadFileForm()})
