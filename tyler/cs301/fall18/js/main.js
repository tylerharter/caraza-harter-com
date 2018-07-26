$(function() {
    function main() {
	get_nav()
    }

    function get_nav() {
	$("#navbarCollapse").load("nav.html", got_nav);
    }

    function got_nav() {
	var curr_page = window.location.pathname.split('/').slice(-1)[0]
	$('.nav-link').each(function(i,link) {
	    var curr_link = link.href.split('/').slice(-1)[0]

	    if (curr_link == curr_page) {
		$(link).parent().addClass("active")
	    }
	});
    }

    main()
});
