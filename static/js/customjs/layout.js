$(document).ready(function() {

	$('#loginform').on('submit', function(event) {

		$.ajax({
			data : {
				username : $('#username').val(),
				password : $('#password').val()
			},
			type : 'POST',
			url : '/login'
		})
		.done(function(data) {

			if (data.success) {
                            $(location).attr('href','/dashboard/1')
			}
			else {
				alert("something wrong")
			}

		});

		event.preventDefault();

	});

});