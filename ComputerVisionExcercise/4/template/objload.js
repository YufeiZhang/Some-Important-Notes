// Global var definition
var camera, scene, renderer;
var fileData;
var vertics=[];
var face=[];
var reader= new FileReader();
var isWireframe = true;
var material = new THREE.MeshBasicMaterial({ color: 0xffffff });
material.wireframe = true;


// Your Methods 
window.addEventListener("load", onDragListener, false);


function getFile(line) {
	fileData = line.split(/\r?\n/);

	for (index = 0; index < fileData.length; ++index) {
    	if (fileData[index].charAt(0) == "v"){
    		fileData[index]=fileData[index].substring(2);
    		vertics.push(fileData[index]);
    	}
    	else if (fileData[index].charAt(0) == "f"){
    		fileData[index]=fileData[index].substring(2);
    		face.push (fileData[index]);
    	}
	}

	initialize();
}


function drag(event) { 
    // Get the file you drag
	var files = event.dataTransfer.files[0]; 
	event.stopPropagation(); 
	event.preventDefault(); 
	
	reader.onload=function(e) {
	 	fileData=reader.result;
	 	getFile(fileData);
	};
	reader.readAsText(files);
}


function onDragListener() { 
 	var container = document.getElementById("centered"); 
 	
 	// run when you drag the object
 	container.addEventListener("dragenter", function(event) { 
 		event.stopPropagation(); 
 		event.preventDefault(); 
 	}, false);

	// run when you drag to the right place
	container.addEventListener("dragover", function(event) { 
 		event.stopPropagation(); 
 		event.preventDefault(); 
 	}, false); 

 	// run when drag is done
 	container.addEventListener("drop", drag, false);
 } 


function onWindowResize() {
	var canvasWidth = window.innerWidth;
	var canvasHeight = window.innerHeight;

	renderer.setSize( canvasWidth, canvasHeight );

	camera.aspect = canvasWidth / canvasHeight;
	camera.updateProjectionMatrix();

	render();
}


/** Switch between solid and wireframe modes */
function switch_display() {
	if (isWireframe) {
		isWireframe = false;
		material.wireframe = false;
	} else {
		isWireframe = true;
		material.wireframe = true;
	}
}


/** Initialize Three.js objs */
function initialize() {
	container = document.getElementById("webgl");
	document.body.appendChild( container );	
	var width = container.clientWidth;
	var height = container.clientHeight;
	var x,y,z;
	var xf,yf,zf;
	document.getElementById("centered").style.display='none';

	// Create camera and move it along the z-axis
	camera = new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,80000);
	camera.position.z = 15;
	scene = new THREE.Scene();

	var geometry = new THREE.Geometry();

	for (index = 0; index < vertics.length; index++){
		var buff=vertics[index].split(" ");
		x=buff[0];
		y=buff[1];
		z=buff[2];
		geometry.vertices.push( new THREE.Vector3(x, y, z));
	}

	for (index = 0; index < face.length; index++){
		var buff1=face[index].split(" ");
		xf=buff1[0]-1;
		yf=buff1[1]-1;
		zf=buff1[2]-1;
		geometry.faces.push( new THREE.Face3(xf, yf, zf));
	}

	geometry.computeBoundingSphere();

 	var obj = new THREE.Mesh(geometry, material);
	scene.add(obj);

	// and the camera
	scene.add(camera);
	var ambient = new THREE.AmbientLight( 0x101030 );
	scene.add( ambient );

	var directionalLight = new THREE.DirectionalLight( 0xffeedd );
	directionalLight.position.set( 0, 0, 1 );
	scene.add( directionalLight );

	// draw!
	renderer= new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth,window.innerHeight);
	renderer.setClearColor( 0xAAAAAA );
	renderer.gammaInput = true;
	renderer.gammaOutput = true;
	container.appendChild(renderer.domElement);
	requestAnimationFrame( render );
	renderer.render(scene, camera);
	window.addEventListener( 'resize', onWindowResize, false );

	// CONTROLS
	cameraControls = new THREE.OrbitControls( camera, renderer.domElement );
	cameraControls.target.set( 0, 0, 0 );
	cameraControls.addEventListener('change', render);
}


var render = function () {
	requestAnimationFrame( render );
	renderer.render(scene, camera);
};


/** Called when page is loaded */
function load() {

}

