/*
 * Notifyjs - A Java Script Notification plugin
 * This plugin tries to emulate toast and snackbar notification components found in Google Material Design
 * 
 */
(function(){
	
	var css =
	".notifyjs-notification-center{display:inline-block;position: fixed;bottom: 0;z-index: 99999;overflow: hidden;background-color:red;}\
	 .notifyjs-is-mobile{right: 0;left: 0;width: 100%;} \
	 .notifyjs-is-not-mobile{width: 568px;}\
	 .notifyjs-notification{font-size:14px;display: none;cursor: pointer;margin: 0;padding:14px 24px;height: 48px;min-width: 288px;border-radius: 2px;white-space:nowrap;overflow: hidden;text-overflow: ellipsis;}";
	
	//create a style element and inject css into the head
	var style = document.createElement("style");
		style.innerHTML = css;
	document.head.appendChild(style);
	
	//the device's viewport
	var screen_width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
	
	//fallback for ie<=8, use attachEvent and detachEvent instead
	var fallback = !(document.addEventListener && document.removeEventListener);
	
	
	//The Global notification-center object
	//This prevents re-creation of a holder object each time notify is called
	var notificationCenter = document.createElement("div");
	notificationCenter.className  = "notifyjs-notification-center";
	
	//for mobile devices -- width less than 768px -- smartphones and tablets
	if(screen_width < 768)
		notificationCenter.className += " notifyjs-is-mobile";
	else {
		notificationCenter.className += " notifyjs-is-not-mobile";
		
		//to centralise the notification-center
		var offset = (screen_width - 568) / 2;		//568 because it is the width specified in the class				
		notificationCenter.style.marginLeft = offset + "px";
	}
	
	document.body.appendChild(notificationCenter);
	
	
	//Global notifications function
	notifyjs_queue = [];
	
	//this function creates a notification object and adds it to the notifications queue
	window.notify = function(text, params){
		
		var defaults = {
			duration: 5000,				//5 seonds default
			onAction: null,				//fired when notification is clicked
			onFinish: function(){ },	//fired in the end
			
			//Customisation
			backgroundColor: "#323232",
			color: "#FFF"
		};
		
		var notifyjs = {};
		notifyjs.setting = extend({}, defaults, params);
		notifyjs.notification = notificationBuilder(text, notifyjs.setting.onAction, notifyjs.setting.backgroundColor, notifyjs.setting.color);
		
		addToNotificationQueue(notifyjs);
	}	
	
	
	//Notification object builder
	function notificationBuilder(text, onAction, bg, cl){
		//create the notfication object
		var obj = document.createElement("div");
			obj.className = "notifyjs-notification";
			obj.innerHTML = text;
			obj.style.backgroundColor = bg;
			obj.style.color = cl;
		
		//add an onAction listener
		if(onAction != null && typeof onAction == "function"){	//create an action handler, only if handler is supplied
			oneTime(obj, "click", fallback, onAction);
		}
		
		return obj;
	}
	
	//adds the notiication to global notification queue
	function addToNotificationQueue(obj){
		notifyjs_queue.push(obj);
		if(notifyjs_queue.length === 1) processNotificationQueue();		//instantly process the notification
	}
	
	//show the next notifictaion in the queue
	function processNotificationQueue(){
		if(notifyjs_queue.length === 0)return;

		var obj = notifyjs_queue[0];	//first object from queue
		
		//append the object to center and display it
		notificationCenter.appendChild(obj.notification);
		obj.notification.style.display = "block";
		
		//add a timer to remove the object and process another object from the queue
		setTimeout(function(){
			//remove the object
			obj.notification.style.display = "none";
			notificationCenter.removeChild(obj.notification);
			
			//remove it from queue  as well
			notifyjs_queue.splice(0,1);
			
			//fire onFinish
			obj.setting.onFinish();
			
			//goto next
			processNotificationQueue();
			
		}, obj.setting.duration);
	}
	
	
/* UTILITY FUNCTIONS */
	//Re-creation of jQuery.extend to remove un-necessary dependency
	//taken from http://youmightnotneedjquery.com/#extend
	function extend(out){
		var out = out || {};
		
		for(var i=1; i<arguments.length; i++){
			var obj = arguments[i];
			
			if(!obj)continue;
			
			for(var key in obj){
				if(obj.hasOwnProperty(key))
					out[key] = obj[key];
			}
		}
		
		return out;
	}
	
	//One time event handle
	function oneTime(node, type, ie, callback){
		
		if(ie === true){
			node.attachEvent(type, function(evt){
				///remove listener
				evt.target.detachEvent(evt.type, arguments.callee);
				//call handler
				return callback(evt);
			});
		} else {
			node.addEventListener(type, function(evt){
				//remove listener
				evt.target.removeEventListener(evt.type, arguments.callee);
				//call handler
				return callback(evt);
			});
		}
	}
	
	
}());