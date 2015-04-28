# -- CoffeeScript Code ---

root = this
root.UI = {}
root.Chat = {}


# ==================== UTILS =============================


delay = (ms, func) -> setTimeout func, ms
repeat = (ms, func) -> setInterval func, ms

# Read a cookie helper
getCookie = (key) ->
    r = document.cookie.match("\\b" + key + "=([^;]*)\\b")
    if r then r[1]


# Wrapper around $.ajax get
getJSON = (url, before) ->
    xsrf = getCookie '_xsrf'
    headers = 'X-XSRFToken': xsrf
    args =
        url: url
        dataType: 'json'
        headers: headers
        beforeSend: before
    $.ajax args

# Wrapper around $.ajax post
postJSON = (url, data, before) ->
    xsrf = getCookie '_xsrf'
    headers = 'X-XSRFToken': xsrf
    args =
        url: url
        method: 'post'
        dataType: 'json'
        data: JSON.stringify data
        headers: headers
        beforeSend: before
    $.ajax args


# ======================================================

# Build relative dates
UI.buildRelativeDates = (selector) ->
    s = if selector then selector else '.timestamp'
    dates = $(s)
    _.each dates, (item) ->
        date = new Date $(item).html() * 1000
        $(item).html(moment(date).fromNow())


UI.buildRelativeDates()



# ==================== CHANNEL =============================


SOCKET_STATES = {connecting: 0, open: 1, closing: 2, closed: 3}

class Channel

    callbacks: null
    states: SOCKET_STATES

    constructor: (address, opts = {}) ->
        @socket = new WebSocket address
        @opts = opts
        @reset()

    on: (event, callback) ->
        @callbacks.push({event, callback})

    reset: ->
        @callbacks = []
        @connect()
        @pings()


    send: (msg) ->
        payload = JSON.stringify(msg)
        if @socket.readyState is @states.open
            @socket.send(payload)
        else
            console.log 'Cannot send message. ws state: ', @socket.readyState

    onOpen: ->
        console.log 'ws connection openned ...'

    onClose: ->
        console.log 'ws connection closed ...'

    onError: (error) ->
        console.log 'ws error', error

    onMessage: (event) ->
        payload = JSON.parse(event.data)
        @trigger(payload.event, payload.msg)

    trigger: (eventName, msg) ->
      callback(msg) for {event, callback} in @callbacks when event is eventName

    pings: ->
        repeat 5000, =>
            console.log 'Send server pings ...'
            @send({event: 'ping', msg: null})

    connect: ->
        @socket.onopen = () => @onOpen()
        @socket.onclose = (event) => @onClose()
        @socket.onerror = (error) => @onError(error)
        @socket.onmessage = (event) => @onMessage(event)


# ==================== BACKBONE APP =============================


# Overwrite sync routine to include xsrf cookie
backboneSync = Backbone.sync
Backbone.sync = (method, model, options) ->
    xsrf = getCookie '_xsrf'
    options.headers = 'X-XSRFToken': xsrf
    return backboneSync(method, model, options)


class Message extends Backbone.Model
    idAttribute: 'key'


class MessageView extends Backbone.View
    model: Message

    template: (m) -> _.template($('#message-template').html())(m)

    initialize: ->
        this.listenTo(this.model, 'change', this.render)

    render: ->
        this.$el.html this.template this.model.toJSON()
        return this


class AppView extends Backbone.View
    el: $('body')
    events: {
        'keypress #new-message': 'sendMessage'
    }

    initialize: (opts) ->
        this.input = this.$("#new-message")
        this.channel = opts.channel
        this.startChannel()
        console.log "Backbone application started for channel #{opts.channel} ..."

    startChannel: ->

        app = this

        if this.channel

            this.channel = new Channel "ws://localhost:8001/ws/#{this.channel}"

            this.channel.on 'new_msg', (msg) =>
                app.showMessage(msg)

            this.channel.on 'pong', (msg) ->
                console.log 'Pong'

        else
            console.log 'No ws for you, since you dont have a channel'

    ping: ->
        this.channel.send({event: 'ping', msg: null})

    showMessage: (msg) ->
        view = new MessageView({model: msg})
        console.log 'View is', view
        this.$("#messages").append(view.render().el)

    sendMessage: (e) ->
        if e.which is 13
            msg = {text: $(e.target).val(), timestamp: Number(new Date())}
            payload = {event: 'new_msg', msg: msg}
            this.channel.send payload
            this.input.val('')


root.Chat.AppView = AppView
