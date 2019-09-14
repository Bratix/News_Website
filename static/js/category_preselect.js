$(document).ready(function(){
    var cat = $(".category_preselected").data("value")
    $(".category_preselected").val(cat);

    $("[name=picture-clear]").css({'height':'20px','margin-bottom':'0px','display':'inline'})
})