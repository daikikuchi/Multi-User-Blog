$(function() {
    // Toggle display of editing form and comment div
    $('.comment-list').on('click', '.comment-link-edit', function(e) {
        e.preventDefault();
        $(this).closest('.single-comment').next('.comment-edit-form').toggle('display');
        $(this).closest('.single-comment').toggle('display');
    });
    // Cancel editing a comment
    $('.comment-list').on('click', '.cancel-comment', function(e) {
        e.preventDefault();
        $(this).closest('.comment-edit-form').toggle('display');
        $(this).closest('.comment-edit-form').prev('.single-comment').toggle('display');
    });
});