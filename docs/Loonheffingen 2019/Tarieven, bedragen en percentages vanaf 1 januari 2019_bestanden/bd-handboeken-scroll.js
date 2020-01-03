
function setScrolling() {

    var heightWindow        = $(window).height();
    var heightHeader        = $('#content .header').innerHeight();
    var heightBreadcrumb    = $('#content .breadcrumb').innerHeight();
    var heightFooter        = $('.footer').innerHeight();

    var paddingBody         = $('.handboek').innerHeight() - $('.container').innerHeight();
    var paddingWrappers     = $('.content_wrapper1').innerHeight() - $('.content').innerHeight();

    var heightToSubstract   = heightHeader + heightFooter + paddingWrappers + paddingBody - 15;
    var heightContent       = heightWindow - heightToSubstract;
    var heightLeft          = heightContent;
    var heightRight         = heightContent - heightBreadcrumb;

    $('.last')          .css("min-height"   , heightRight   + "px");
    $('.content')       .css("height"       , heightContent + "px");
    $('.content .left') .css("max-height"   , heightLeft    + "px");
    $('#hoofd_content') .css("max-height"   , heightRight   + "px");
}
$("#bd-nojs").remove();
setScrolling();

$(window).resize(function() {
    setScrolling();
});
