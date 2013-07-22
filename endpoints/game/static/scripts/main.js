var sock_url = '/socket';
var sock = new SockJS(sock_url);

var multiplexer = new WebSocketMultiplex(sock);
var username_sock = multiplexer.channel('username');
var gamelist_sock = multiplexer.channel('gamelist');

var secret = '';

gamelist_sock.onopen= function(evt) {
	gamelist_sock.send(JSON.stringify({
		'action': 'get_list'
	}));
};

username_sock.onmessage = function(evt) {
	obj = $.parseJSON(evt.data);
	if (obj.status == 'error'){
		$('div#username div.error').html('Error: ' + obj.errormsg);
	}
	else {
		secret = obj.secret;
		$('div#username div.error').html('Hi, ' + obj.username + '. Your secret key is ' + secret);
	}
};

gamelist_sock.onmessage = function(evt) {
	obj = $.parseJSON(evt.data);
	$('div#gamelist textarea').html('');
	$.each(obj.games, function(index, value) {
		$('div#gamelist textarea').append(index + ': ' + value.username + '\n');
	});
};

$(function() {
	$('div#username input[type="submit"]').on('click', function() {
		username = $('div#username input[type="text"]').val();
		username_sock.send(JSON.stringify({
			'action': 'select_username',
			'username': username
		}));
	});

	$('div#gamelist button#create_new_game').on('click', function() {
		console.log({
			'action': 'create_game',
			'secret': secret,
			'username': username
		});
		gamelist_sock.send(JSON.stringify({
			'action': 'create_game',
			'secret': secret,
			'username': username
		}));
	});
});