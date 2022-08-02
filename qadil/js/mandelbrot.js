     function plotGraph(){
         xmin = -2;
         xmax = 0.5;
         ymin = -1.25;
         ymax = 1.25;

	 var g = Mandelbrot("sceneniels");
	 
	 g.init(xmin, xmax, ymin, ymax);
	 
	 g.plot();
	 
	 Overlay("overlayniels", g);
     }

    var Mandelbrot = function(canvasid){
    
    var functionstring, // function expression as string 
	xmin,
	xmax,
	dx,
	ymin,
	ymax,
	dy,
	canvas,
	ctx,
	width,
	height,
	colors;
    
    colors = Math.pow(2, 64);
    colorsStep = colors/1000;
    
    canvas = document.getElementById(canvasid);
    width = canvas.width;
    height = canvas.height;
    ctx = canvas.getContext('2d');
    
    
    var convertrgb = function(num){
	var n = num, x, y, z;
	
	z = n % 256;
	n = (n - z)/256;
	y = n % 256;
	n = (n - y)/256;
	x = n %256;
	
	return{
	    rr: x,
	    gg: y,
	    bb: z
	}
	
    }
    
    var graphinit = function(xmi, xma, ymi, yma){
	xmin = xmi;
	xmax = xma;
	ymin = ymi;
	ymax = yma;
	dx = xmax - xmin;
	dy = ymax - ymin;
    }
    
    var canvasTocoord = function(x, y){
	return {
	    x: dx * x/width + xmin, 
	    y:-dy * y/height + ymax
	}
    }
    
    
    var insideSet = function(x0, y0){
	var x = x0, y = y0, x1, y1, i;
     
	for (i = 0; i < 1000; i++){
	    x1 = x*x - y*y;
	    y1 = 2*x*y;
	    x = x1 + x0;
	    y = y1 + y0;
	    if (x*x + y*y > 4)
		break;
	}
	
	return (i);
    }
    
    var plotgraph = function(){
	var x, y, v, noOfiter, col;
	
	
	ctx.clearRect(0,0, width, height);	
	
	ctx.beginPath();
	for(x = 0; x < width; x++)
	    for(y = 0; y < height; y++){
		v = canvasTocoord(x, y);
		noOfiter = insideSet(v.x, v.y);
		
		{
		    //col = convertrgb((1000 - noOfiter) * colorsStep);
		    col = convertrgb((1000 - noOfiter)*1000); // frosty night
		    //col = convertrgb((1000 - noOfiter)*10000);
		    ctx.fillStyle =
			"rgb(" + col.rr + "," + col.gg + "," +  col.bb + ")";
		    ctx.fillRect(x, y, 1, 1);
		}
	    }
        ctx.stroke();		
        

	
    }
    
    
    return {	
	// Functions
	
	init: graphinit,
	plot: plotgraph,
	canvasTocoord: canvasTocoord
    };
}


var Overlay = function(canvasid, g){
    var
    canvas,
    x0,
    y0,
    mouseDown;
    
    mouseDown = false;
    canvas = document.getElementById(canvasid); 
    ctx = canvas.getContext("2d");

    canvas.addEventListener("mousedown", function(evt){
	x0 = evt.clientX; y0 = evt.clientY; // Where are we at down?
        var rect = canvas.getBoundingClientRect();
        
        x0 = x0 - rect.left; y0 = y0 - rect.top;
	mouseDown = true;
    });
    
    canvas.addEventListener("mousemove", function(evt){
	if (mouseDown)
	{
	    var ctx = canvas.getContext("2d");
            var rect = canvas.getBoundingClientRect();
	    // Clear canvas:
	    
	    ctx.clearRect(0,0, canvas.width, canvas.height);	
	    
	    ctx.beginPath();
	    ctx.rect(x0, y0, (evt.clientX-rect.left)- x0, (evt.clientY-rect.top) - y0);
	    ctx.strokeStyle='red';
	    ctx.stroke();
	    
	};
    });
    
    
    canvas.addEventListener("mouseup", function(evt){
	var v0, v1, xmin, xmax, ymin, ymax, ctx;
	
	mouseDown = false;
	
	ctx = canvas.getContext("2d");
	
        var rect = canvas.getBoundingClientRect();

	v0 = g.canvasTocoord(x0, y0);
	v1 = g.canvasTocoord(evt.clientX-rect.left, evt.clientY-rect.top);
	
	if (v1.x > v0.x){
	    xmax = v1.x;
	    xmin = v0.x;
	}
	else {
	    xmax = v0.x;
	    xmin = v1.x;
	}
	
	if (v1.y > v0.y){
	    ymax = v1.y;
	    ymin = v0.y;
	}
	else {
	    ymax = v0.y;
	    ymin = v1.y;
	}
	
	
	ctx.clearRect(0,0, canvas.width, canvas.height);	
	
	g.init(xmin, xmax, ymin, ymax);		
	g.plot();	
	
    });
}

plotGraph();


