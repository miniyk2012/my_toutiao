var $likeBtn = $('.like-button');
var $isLiked = $likeBtn.hasClass('liked');
var $collectBtn = $('.collect-button');
var $isCollected = $collectBtn.hasClass('collected');

$likeBtn.on('click', (event)  => {
    let $this = $(event.currentTarget);
    let url = $this.data('url');

    $.ajax({
        url: `/api/${url}`,
        type: $isLiked ? 'DELETE' : 'POST',
        data: {},
        success: function(rs) {
            if (!rs.r) {
                let isLiked = rs.data.is_liked;
                if ($isLiked != isLiked) {
                    $isLiked = isLiked;
                    $this.toggleClass('liked');
                }
            } else {
                alert('点赞失败, 请稍后再试');
            }
        }
    });
});


$collectBtn.on('click', (event)  => {
    let $this = $(event.currentTarget);
    let url = $this.data('url');

    $.ajax({
        url: `/api/${url}`,
        type: $isCollected ? 'DELETE' : 'POST',
        data: {},
        success: function(rs) {
            if (!rs.r) {
                let isCollected = rs.data.is_collected;
                if ($isCollected != isCollected) {
                    $isCollected = isCollected;
                    $this.toggleClass('collected');
                }
            } else {
                alert('收藏失败, 请稍后再试');
            }
        }
    });
});
