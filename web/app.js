function init(){
    // Does the Thing
}


//////////////////////////////////////////////////////////////////
// Initialisation

if (!window.requestAnimationFrame){

    window.requestAnimationFrame = (function(){
    	return	window.webkitRequestAnimationFrame  ||
        		window.mozRequestAnimationFrame		||
        function( callback ){
        	window.setTimeout(callback, 1000 / 60);
    	};
    })();
}

var PIXEL_RATIO = (function () {
    var ctx = document.createElement("canvas").getContext("2d"),
        dpr = window.devicePixelRatio || 1,
        bsr = ctx.webkitBackingStorePixelRatio ||
              ctx.mozBackingStorePixelRatio ||
              ctx.msBackingStorePixelRatio ||
              ctx.oBackingStorePixelRatio ||
              ctx.backingStorePixelRatio || 1;

    return dpr / bsr;
})();


function canvas_setup(){
    c = document.getElementById("main_c");

    // Make the main canvas visually fill the positioned parent
    c.style.width ='100%';
    c.style.height='100%';
    // ...then set the internal size to match

    // make a HD canvas
    c.width = c.offsetWidth * PIXEL_RATIO;
    c.height = c.offsetHeight * PIXEL_RATIO;
    c.getContext("2d").setTransform(PIXEL_RATIO, 0, 0, PIXEL_RATIO, 0, 0);

/*
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
*/

    if (c == undefined){
        document.getElementById("defaultPara").innerHTML = "Sorry, \
        your browser doesn't seem to support the canvas element from HTML5.\
        Firefox, Chrome, Safari, Opera and Internet Explorer 7+ should work.";
    document.getElementById("defaultPara").innerHTML = '';
    return c;
}

function init(){
    window.canvas = canvas_setup();
    parts.setup(canvas); // Store this data in the object for easy reference

    ctx = canvas.getContext('2d');
    ctx.fillStyle = '#dddddd';
	ctx.fillRect(0,0,canvas.width,canvas.height);

	canvas.addEventListener("click", handleClick);

    gui = new UIData();

    gui.addButton({x: -BSZ - 10, y: -BSZ - 10, width: BSZ, height: BSZ},
        function(e){
            // Play/Pause button
            gs.play = !gs.play;
            gs.selecting = false;
            if (!gs.play) {
                // we just paused
                parts.resetTrucks();
                gs.selecting=true;
            }
            gs.playTime = 0;
            gui.render();
        },
        function(rect){
            // renderer
            var img;
            if (gs.play){
                img = document.getElementById('StopImg');
            } else {
                img = document.getElementById('PlayImg');
            }
            ctx.drawImage(img, rect.x, rect.y, rect.width, rect.height);
        });

    gui.addButton({x: -BSZ -10, y: -2 *(BSZ + 10), width: BSZ, height: BSZ},
            function(e){
                parts.undo();
                gui.render();
            },
        function(rect){
            // renderer
            var img = document.getElementById('UndoImg');
            ctx.drawImage(img, rect.x, rect.y, rect.width, rect.height);
        }
    );

    gui.addButton({x:-BSZ -10, y: 3*(BSZ + 10), width: BSZ, height: BSZ},
        function(e){

        },
        function(rect){
            var img;
            switch (gs.gameMode) {
                case 'time':
                    img = document.getElementById('ClockImg');
                    break;
                case 'distance':
                    img = document.getElementById('RulerImg');
                    break;
                default:
                    img = document.getElementById('UnknownImg');
                    console.log(gs.gameMode);
            }
            ctx.drawImage(img, rect.x, rect.y, BSZ, BSZ);
        }
    );

    var isTime = function(){
        return gs.gameMode == 'time';
    };

    var isDist = function(){
        return gs.gameMode == 'distance';
    }

    gui.addDisplay({x: -50, y: 30}, parts.pathLen, isDist);
    gui.addDisplay({x: -50, y: 49}, "km", isDist);
    gui.addDisplay({x: -50, y: 80}, function(){
        if (gs.play){
            return Math.floor(gs.playTime*2*1.618*0.8158/SPEED_MAX);
        } else {
            return Math.floor(parts.pathTime()*2*1.618);
        }

    }, isTime);
    gui.addDisplay({x: -50, y: 99}, "mins", isTime);


    parts.nextLevel();


    // main loop
    (function animloop(time){
        requestAnimationFrame(animloop);
        if (gs.play){
            gs.playTime += 1;
            parts.update();

            if (!document.hidden){
                gui.render();
                parts.render();
            }
        }
    })();

};
