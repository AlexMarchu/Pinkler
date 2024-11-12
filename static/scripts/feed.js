$(document).ready(function() {
    console.log("Script did!")
    $('.like-form').on('submit', function(event) {
        event.preventDefault();
        const form = $(this);
        const url = form.data('url');
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function(response) {
                const likeIcon = form.find('.uil-heart');
                const likeCount = form.find('.like-count');

                if (response.liked) {
                    likeIcon.addClass('liked');
                } else {
                    likeIcon.removeClass('liked'); 
                }

                likeCount.text(response.number_of_likes);
            }
        });
    });
});

$(document).ready(function() {
    console.log("Script did!");
    $('.bookmark-form').on('submit', function(event) {
        event.preventDefault();
        const form = $(this);
        const url = form.data('url');
        
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function(response) {
                const bookmarkIcon = form.find('i');

                if (response.bookmarked) {
                    bookmarkIcon.addClass('bookmarked');
                } else {
                    bookmarkIcon.removeClass('bookmarked');
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при добавлении закладки:', error);
            }
        });
    });
});

if (document.getElementById('file-upload')) {
    document.getElementById('file-upload').addEventListener('change', function(event) {
        const file = event.target.files[0];
        const previewImage = document.getElementById('preview-image');
        const filePreview = document.getElementById('file-preview');
    
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result; 
                filePreview.style.display = 'block'; 
            }
            reader.readAsDataURL(file);
        } else {
            filePreview.style.display = 'none'; 
        }
    });
}

if (document.getElementById('remove-file')) {
    document.getElementById('remove-file').addEventListener('click', function() {
        const fileUpload = document.getElementById('file-upload');
        const filePreview = document.getElementById('file-preview');
    
        fileUpload.value = '';
        filePreview.style.display = 'none'; 
    });
}

$( document ).ready(function() {
    let display = false
    $(".cmt_btn").click(function () {
        if (display===false) {
            $(this).next(".comment-box").show("slow");
            display=true
        } else {
            $(this).next(".comment-box").hide("slow");
            display=false
        }  
    });
});

$(document).ready(function() {
    // Обработчик клика по кнопке "Создать пост"
    $("#create-post").click(function() {
        // Перемещение фокуса на текстовое поле контента поста
        $("#post-form-content").focus(); // Используйте ID поля
    });
});