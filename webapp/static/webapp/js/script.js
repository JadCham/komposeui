function reset_ui(){
    $("#success_div").fadeOut("fast", function() {
        $("#strong_success").text("Success! ");
    });
    $("#failure_div").fadeOut("fast", function() {
        $("#strong_failure").html("");
    });
    $("#warning_div").fadeOut("fast", function() {
        $("#strong_warning").html("");
    });
    $("#output").html("");

}

function checkValidYamlInput(){
    try {
        var doc = jsyaml.safeLoad($('#input').val());
        if ($('#input').val().length >0 && typeof doc == "object"){
            return true;
        }
    }
    catch(err) {

        $("#failure_div").fadeIn("fast", function () {
            $("#strong_failure").text("Not a valid yaml input");
        });
    }
    return false;
}
function callServerScript() {
    if (checkValidYamlInput()){
        // reset_ui();
        $('#converter').submit();
    }
}
$( document ).ready(function() {
    $("#download_button").click(function () {
        reset_ui();
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
                    var result = JSON.parse(data["data"]);
                    $("#success_div").fadeIn("fast", function () {
                        $("#strong_success").text($("#strong_success").text()+data["status"]);
                    });
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

                            $("#warning_div").fadeIn("fast", function () {
                                $("#strong_warning").html(result["fields"]["warning"]);
                            });
                        }
                        if (data["input_file"]){
                            $('#input').val(data["input_file"]);
                        }
                    }
                }
                else{

                    $("#failure_div").fadeIn("fast", function() {
                        $("#strong_failure").html(data["status"]);
                    });
                }
            },
            error: function () {

                $("#failure_div").fadeIn("fast", function() {
                    $("#strong_failure").html("Could not connect to server!");
                });
            }
        });
        return false;
    });
});
