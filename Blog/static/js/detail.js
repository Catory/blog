$(function () {
    $('.collect').click(function () {
        // $(this).removeClass('glyphicon glyphicon-heart-empty');
        var id = $('#postid').val();
        // console.log(id);

        // var url = 'http://127.0.0.1:8000/blog/collect/%d/'%(id);
        var url = 'http://127.0.0.1:8000/blog/collect/'+id;
        // console.log('11111111111111',url);
        $.get(url,function (result) {
            console.log(result);
            if(result.status==='remove'){
                $('.collect').text('收藏');

            }
            else {
                $('.collect').text('取消收藏');

            }
        });

    })
});