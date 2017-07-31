function reset_ui(){
    $("#success_div").fadeOut("slow", function() {
        $("#strong_success").text("Success! ");
    });
    $("#failure_div").fadeOut("slow", function() {
        $("#strong_failure").text("");
    });
    $("#warning_div").fadeOut("slow", function() {
        $("#strong_warning").text("");
    });
    $("#output").html("");

}
function callServerScript() {
    try {
        var doc = jsyaml.safeLoad($('#input').val());
        if ($('#input').val().length >0 && typeof doc == "object"){
            $('#converter').submit();
        }
    }
    catch(err) {
        $("#strong_failure").text("Not a valid yaml input");
        $("#failure_div").fadeIn("slow");
    }
}
$( document ).ready(function() {
    $("#download_button").click(function () {
        $("#file_upload").val("1");
        $('#converter').submit();
    });
    new Clipboard('.btn');
    var searchTimeout;
    $('#input').bind('input propertychange', function() {
        reset_ui();
        if (searchTimeout != undefined) clearTimeout(searchTimeout);
        searchTimeout = setTimeout(callServerScript, 500);
    });
    var frm = $('#converter');
    frm.submit(function () {
        reset_ui();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: new FormData($("form")[0]),
            processData: false,
            contentType: false,
            success: function (data) {
                if (data["success"]){
                    $("#strong_success").text($("#strong_success").text()+data["status"]);
                    $("#success_div").fadeIn("slow");
                    var result = JSON.parse(data["data"]);
                    // Handle Files
                    if ($("#file_upload").val()==1){
                        var file = window.location.origin+ "/" + result["fields"]["output_file"];
                        download(file);
                        $("#id_input_file").val("");
                        $("#file_upload").val("");
                    }
                    // Handle text
                    else{
                        var formatted = Prism.highlight(result["fields"]["output_text"], Prism.languages.yaml);
                        $("#output").html(formatted);
                        $("#download_button").attr('name', result["fields"]["output_file"]);
                        if (result["fields"]["warning"]){
                            $("#strong_warning").html(result["fields"]["warning"]);
                            $("#warning_div").fadeIn("slow");
                        }
                        if (data["input_file"]){
                            $('#input').val(data["input_file"]);
                        }
                    }
                }
                else{
                    $("#strong_failure").html($("#strong_failure").html()+data["status"]);
                    $("#failure_div").fadeIn("slow");
                }
            },
            error: function () {
                $("#strong_failure").html("Could not connect to server!");
                $("#failure_div").fadeIn("slow");
            }
        });
        return false;
    });
});
