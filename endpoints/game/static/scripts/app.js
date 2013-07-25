var sock_url = '/socket';
var sock = new SockJS(sock_url);

var multiplexer = new WebSocketMultiplex(sock);
var username_choice_sock = multiplexer.channel('username_choice');

$(function() {

// Create app object for isolated scope/namespace.
window.app = {
	el: $("#app"),
	view: {},
	currentView: null,
	socket: null,

	init: function() {
		app.goto("nickname");
	},

	goto: function(view, model) {
		if ((this.currentView !== null) && (this.currentView.empty != "undefined")) {
			app.view[this.currentView].empty();
			app.view.error.empty();
		}

		this.currentView = view;
		app.view[view].init(model);
	}
};


// Error view.
app.view.error = {
	el: $("#error"),
	template: $("#tpl-error").html(),
	model: [],

	init: function(model) {
		this.model = model || this.model;
		this.render();
	},

	render: function() {
		if (!this.model.length) {
			return;
		}
		this.el.html(Mustache.render(this.template, this.model));
	},

	empty: function() {
		this.el.empty();
	}
};

// Nickname view.
app.view.nickname = {
	el: $("#nickname"),
	template: $("#tpl-nickname").html(),

	init: function() {
		this.render();

		username_choice_sock.onmessage = function(evt) {
			obj = $.parseJSON(evt.data);
			if (obj.status == 'error'){
				app.view.error.init(obj.errors);
			}
			else{
				console.log("Go to the next...");
			}
		};

	},

	events: function() {
		var self = this;

		$("#nickname-username").keyup(function(e) {
			if(e.keyCode == 13) {
				username_choice_sock.send(
					JSON.stringify(
						self.serialize()
					)
				);
			}
		});
	},

	render: function() {
		this.el.html(Mustache.render(this.template, {}));
		this.events();
	},

	serialize: function() {
		var username = $('#nickname-username').val();
		return {
			"username": username
		};
	},

	empty: function() {
		this.el.empty();
	}
};

// Initialize app.
app.init();

});