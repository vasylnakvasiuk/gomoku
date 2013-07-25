var sock_url = '/socket';
var sock = new SockJS(sock_url);

var multiplexer = new WebSocketMultiplex(sock);
var usernameChoiceSock = multiplexer.channel('username_choice');
var gamesListSock = multiplexer.channel('games_list');
var gamesJoinSock = multiplexer.channel('games_join');
var gameCreateSock = multiplexer.channel('game_create');


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

		usernameChoiceSock.onmessage = function(evt) {
			obj = $.parseJSON(evt.data);
			if (obj.status == 'ok'){
				app.secret = obj.secret;
				app.username = obj.username;
				app.goto("games");
			}
			else {
				app.view.error.init(obj.errors);
			}
		};

	},

	events: function() {
		var self = this;

		$("#nickname-username").keyup(function(e) {
			if (e.keyCode == 13) {
				usernameChoiceSock.send(
					JSON.stringify(self.serialize())
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

// Games view.
app.view.games = {
	el: $("#games"),
	templates: {
		"main": $("#tpl-games").html(),
		"list": $("#tpl-games-choose-container").html()
	},
	model: [],

	init: function(model) {
		this.model = model || this.model;
		this.render();

		if (model !== undefined) {
			this.updateModel(model);
		} else {
			gamesListSock.send(
				JSON.stringify(
					{"secret": app.secret}
				)
			);
		}

		var self = this;
		gamesListSock.onmessage = function(evt) {
			obj = $.parseJSON(evt.data);
			if (obj.status == 'ok'){
				self.updateModel(obj.games);
			}
			else {
				app.view.error.init(obj.errors);
			}
		};

		gamesJoinSock.onmessage = function(evt) {
			obj = $.parseJSON(evt.data);
			if (obj.status == 'ok'){
				console.log("Go to the next...");
			}
			else {
				app.view.error.init(obj.errors);
			}
		};

	},

	events: function() {
		var self = this;

		$('#games-join').click(function() {
			gamesJoinSock.send(
				JSON.stringify(self.serialize())
			);
		});

		$('#games-create').click(function() {
			app.goto("details");
		});
	},

	render: function() {
		this.el.html(Mustache.render(this.templates["main"], {}));
		this.renderList();
		this.events();
	},

	renderList: function() {
		var context;

		if (this.model.length) {
			context = {
				"data": {
					loop: this.model
				}
			};
		} else {
			context = {
				"data": this.model
			};
		}

		$('#games-choose-container').html(Mustache.render(this.templates["list"], context));
	},

	serialize: function() {
		return {
			"secret": app.secret,
			"id": $('#games-choose').val()
		};
	},

	updateModel: function(model) {
		this.model = model || this.model;
		this.renderList();
	},

	empty: function() {
		this.el.empty();
	}
};

// Detials view.
app.view.details = {
	el: $("#details"),
	template: $("#tpl-details").html(),

	init: function() {
		this.render();

		gameCreateSock.onmessage = function(evt) {
			obj = $.parseJSON(evt.data);
			if (obj.status == 'ok'){
				console.log("Go to the next...");
			}
			else {
				app.view.error.init(obj.errors);
			}
		};
	},

	events: function() {
		var self = this;

		$('#details-create').click(function() {
			gameCreateSock.send(
				JSON.stringify(self.serialize())
			);
		});
	},

	render: function() {
		this.el.html(Mustache.render(this.template, {}));
		this.events();
	},

	serialize: function() {
		return {
			"secret": app.secret,
			"dimensions": $('#details-dimensions').val(),
			"lineup": $('#details-lineup').val(),
			"type": $('#details-type').val()
		};
	},

	empty: function() {
		this.el.empty();
	}
};

// Initialize app.
app.init();

});