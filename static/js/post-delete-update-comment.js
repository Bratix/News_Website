//post comment
$(document).ready(function(){

    $(".comment-form").submit(function(e){
        e.preventDefault()
        e.stopImmediatePropagation()

        var text = $('#id_comment_text').val()
        var url = $(this).data("action")
        var token = $("input[name='csrfmiddlewaretoken']").val()

        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            dataType: "json",
            url: url,
            data: {
                comment_text: text,
            },
            
        }).done(function(data){
            
            var monthNames = [
                "JAN", "FEB", "MAR",
                "APR", "MAY", "JUN", "JUL",
                "AUG", "SEP", "OCT",
                "NOV", "DEC"
              ];

            var date = new Date(data.creation_date);
            $('#id_comment_text').val("")
            $('#comment-count').text(data.comment_count)
            if (data.comment_count == 1) {
                $('#comment-count-main').text(data.comment_count+ " komentar")
            }   else {
                $('#comment-count-main').text(data.comment_count+ " komentara")
            }
            

            var Com = $("#emptycom").clone().attr('id','comment'+data.pk).fadeIn(600)
            Com.find("#comdate").html(('0'+date.getHours()).slice(-2)+":"+('0'+date.getMinutes()).slice(-2)+" | "+date.getDate()+" "+monthNames[date.getMonth()])
            Com.find("#comuser").html(data.user)   
            Com.find("#comtext").html(data.comment_text)
            Com.find('#imgLocation').attr('src',data.picture_url)
            
            var durl = Com.find(".btn-cdelete").data('url');
            url_delete = durl.substring(0, durl.length-1)+data.pk
            Com.find(".btn-cdelete").data("url",url_delete)
            Com.find("#comment_text").val(data.comment_text)
            var uurl = Com.find(".update-com").data('url');
            url_update = uurl.substring(0, uurl.length-1)+data.pk
            Com.find('.update-com').data("url",url_update)
            Com.find('.update-com').attr("data-url",url_update)
            console.log(Com)
            $("#comment-area-list").append(Com)

            
        });
    });
})

//Update comment
$(document).ready(function(){

    $("#comment-area-list").on('click','.btn-cupdate',function(e){
        e.preventDefault();
        e.stopImmediatePropagation()

        $(this).closest('li').find('.comment-text-update').removeClass('d-none')
        $(this).closest('li').find('#comtext').addClass('d-none')

        $("#comment-area-list").on('click','.update-com',function(e){
            uurl = $(this).data('url')
            
            comment_text = $(this).closest('div').find('.form-control').val()
            var token = $("input[name='csrfmiddlewaretoken']").val()
            
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": token,
                },
                url: uurl,
                data: {
                    comment_text: comment_text,
                },
            })
            
            $(this).closest('li').find('#comtext').html(comment_text).removeClass('d-none')
            $(this).closest('li').find('.comment-text-update').addClass('d-none')
        })
        
        
    });

});

//delete comment
$(document).ready(function(){

        $("#comment-area-list").on('click','.btn-cdelete',function(e){
            e.preventDefault();
            e.stopImmediatePropagation()
            var url = $(this).data("url")
            var token = $("input[name='csrfmiddlewaretoken']").val()
            var current_comment_count = $("#comment-count").text()
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": token,
                },
                url: url,
            }).done(function(){
                $('#comment-count').text(current_comment_count-1)
                if (current_comment_count-1 == 1) {
                $('#comment-count-main').text(current_comment_count-1 + " komentar")
            }   else {
                $('#comment-count-main').text(current_comment_count-1 + " komentara")
            }
            })
            $(this).closest('li').fadeOut(600)
        });
    
});