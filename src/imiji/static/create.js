var gallery = Object(); // keep track of all data
gallery.title = "";
gallery.images = [];

$(document).ready(function() {
    $("#file_button").on("change", function() {
        handle_files(this.files);
    });

    $("#dropzone").on("dragover", (e) => {
        e.preventDefault();
        e.stopPropagation();
    });

    $("#dropzone").on("dragenter", (e) => {
        e.preventDefault();
        e.stopPropagation();

        $("#dropzone").addClass("shaded");
    });

    $("#dropzone").on("dragexit", (e) => {
        e.preventDefault();
        e.stopPropagation();

        $("#dropzone").removeClass("shaded");
    });

    $("#dropzone").on("drop", (e) => {
        e.preventDefault();
        e.stopPropagation();

        $("#dropzone").removeClass("shaded");

        const files = [];

        const dt = e.originalEvent.dataTransfer;
        // creds to MDN for most of this: https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
        if (dt.items) {
            // Use DataTransferItemList interface to access the file(s)
            for (const item of dt.items) {
                // If dropped items aren't files, reject them
                if (item.kind === "file" && item.type === "image/jpeg") {
                    files.push(item.getAsFile());
                }
            }
        } else {
            // Use DataTransfer interface to access the file(s)
            for (const file of dt.files) {
                if (file.type === "image/jpeg") {
                    files.push(file);
                }
            }
        }

        handle_files(files);
    });

    function handle_files(files) {
        // display new files and add to images list
        for (const file of files) {
            // create and show new image/description textbox
            const new_div = $("#image_template").clone();
            new_div.removeClass("hidden")
            new_div.attr("id", file.name)
            new_div.appendTo("#images");

            // add to images list
            const image = new Object();
            image.file = file;
            image.description = "";
            gallery.images.push(image)

            // read file and save b64 representation
            const reader = new FileReader();
            reader.onload = function(e) {
                $(new_div).find("img").attr("src", e.target.result);
                image.b64 = e.target.result.split("base64,")[1];
            };
            reader.readAsDataURL(file);

            // link description to textarea
            $(new_div).find("textarea").on("change", function() {
                image.description = this.value;
            });
        }
    }

    $("#gallery_title_box").on("change", function() {
        gallery.title = this.value
    });

    $("#upload_button").click(async function() {
        // upload each image
        const uploads = [];
        for (const image of gallery.images) {
            uploads.push(upload_image(image));
        }
        const image_ids = await Promise.all(uploads);
        const gallery_id = await create_gallery(gallery.title, image_ids);
        console.log("All done: ", gallery_id);
    });

    // API call to upload image
    // returns a promise which resolves to the id of the uploaded image
    function upload_image(image) {
        const data = { file: image.b64, description: image.description };

        return fetch("/api/v1.0/upload",
                     {
                       method: "POST",
                       headers: {
                         "Content-Type": "application/json",
                       },
                       body: JSON.stringify(data)
                     })
               .then((response) => response.json())
               .then((data) => {
                 console.log("Image uploaded with id ", data.id);
                 return data.id;
               })
               .catch((error) => {
                 console.error("Error:", error);
               });
    }

    // API call to create gallery
    // returns a promise which resolves to the id of the created gallery
    function create_gallery(title, ids) {
        const data = { title: title, images: ids };

        return fetch("/api/v1.0/gallery/create",
                     {
                       method: "POST",
                       headers: {
                         "Content-Type": "application/json",
                       },
                       body: JSON.stringify(data)
                     })
               .then((response) => response.json())
               .then((data) => {
                 console.log("Gallery created with id ", data.id);
                 return data.id;
               })
               .catch((error) => {
                 console.error("Error:", error);
               });
    }
});
