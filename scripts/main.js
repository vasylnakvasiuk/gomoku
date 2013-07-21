var sock_url = '/socket';
var sock = new SockJS(sock_url);

var multiplexer = new WebSocketMultiplex(sock);
var username_sock = multiplexer.channel('username');
var gamelist_sock = multiplexer.channel('gamelist');

username_sock.onmessage = function(evt) {
	obj = $.parseJSON(evt.data);
	$('div#username div.error').html('Status: ' + obj.status);
};

$(function() {
	$('div#username input[type="submit"]').on('click', function() {
		username = $('div#username input[type="text"]').val();
		username_sock.send(username);
	});
});