//previews the photo before upload, called when picture is selected
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#id_placeholder').attr({'src': e.target.result});
            $('#id_profile').attr({'src': e.target.result});
        }

    reader.readAsDataURL(input.files[0]);
  }
}