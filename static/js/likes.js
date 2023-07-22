$(document).ready(function() {
    // Handle form submission on like/unlike buttons
    $('.like-form').on('submit', function(event) {
        event.preventDefault();
        var likeForm = $(this);
        var post_id = likeForm.data('post-id');
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: '/postslike/' + post_id + '/',
            data: {
                csrfmiddlewaretoken: csrf_token,
            },
            dataType: 'json',
            success: function(response) {
                // Update the like/unlike button based on the JSON response
                if (response.liked) {
                    likeForm.find('button').text('Unlike');
                } else {
                    likeForm.find('button').text('Like');
                }
                // Update the like count
                $('#like-count').text('Likes: ' + response.like_count);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

    // Attach click event handler to the like/unlike button
    $('.like-form').on('click', 'button', function(event) {
        event.preventDefault(); // Prevent the default form submission
        $(this).closest('form').submit(); // Trigger the form submission
    });
});
