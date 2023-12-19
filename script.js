var form = document.getElementById("upload-form");

  
    form.addEventListener("submit", function(event) {
  
      event.preventDefault();
      var fileInput = form.elements["video"];
      var file = fileInput.files[0];
      var formData = new FormData();
      formData.append("video", file);
      var xhr = new XMLHttpRequest();

      xhr.open("POST", "upload.php");

      xhr.addEventListener("load", function() {
        if (xhr.status == 200) {
          document.getElementById("output").innerHTML = xhr.responseText;
        } else {
          document.getElementById("output").innerHTML = "An error occurred while uploading the file.";
        }
      });
      xhr.upload.addEventListener("progress", function(event) {
        if (event.lengthComputable) {
          var percent = (event.loaded / event.total) * 100;
          document.getElementById("progress-bar-value").style.width = percent + "%";
        }
      });
      xhr.send(formData);
    });