import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
// import Button from '@material-ui/core/Button';
import CourtInstructionView from 'views/courtInstructionView';
import * as THREE from 'three';
import GLTF2Loader from 'three-gltf2-loader';
import {courtWidth, courtHeight, rightAngle, courtSpacing} from '../constants';
import canvasToImage from 'canvas-to-image';
GLTF2Loader(THREE);

const colors = {
  random: (arr) => arr[Math.floor(Math.random() * arr.length)],
  court: [0x82E0AA, 0x001f3f, 0x0074D9, 0x7FDBFF, 0x39CCCC, 0x3D9970, 0x2ECC40, 0x01FF70, 0xFFDC00],
  floor: [0x82E0FF, 0xFF851B, 0x85144b, 0xF012BE, 0xB10DC9],
  line: [0xffffff, 0xAAAAAA, 0xDDDDDD]
};

export default class Court extends Component {
  static propTypes = {
    services: PropTypes.object
  };

  constructor(props) {
    super(props);
    this.yaw = 0;
    this.pitch = 0;
    this.loader = new THREE.GLTFLoader();
  }

  bindEvents() {
    this.onMouseDown = this.onMouseDown.bind(this);
    this.onMouseMove = this.onMouseMove.bind(this);
    this.onMouseUp = this.onMouseUp.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
    this.onKeyUp = this.onKeyUp.bind(this);
    this.canvas.addEventListener('mousedown', this.onMouseDown);
    this.canvas.addEventListener('mousemove', this.onMouseMove);
    window.addEventListener('mouseup', this.onMouseUp);
    window.addEventListener('keydown', this.onKeyDown);
    window.addEventListener('keyup', this.onKeyUp);
  }

  unbindEvents() {
    this.canvas.removeEventListener('mousedown', this.onMouseDown);
    this.canvas.removeEventListener('mousemove', this.onMouseMove);
    window.removeEventListener('mouseup', this.onMouseUp);
    window.removeEventListener('keydown', this.onKeyDown);
    window.removeEventListener('keyup', this.onKeyUp);
  }

  onMouseDown(event) {
    this.mouseDown = true;
    this.lastMouseX = event.clientX;
    this.lastMouseY = event.clientY;
  }

  onMouseMove(event) {
    if (!this.mouseDown) {
      return;
    }

    const newX = event.clientX;
    const newY = event.clientY;
    const deltaX = newX - this.lastMouseX;
    const deltaY = newY - this.lastMouseY;

    this.camera.rotation.y -= deltaX * 0.01;
    this.camera.rotation.x -= deltaY * 0.01;
    this.camera.updateProjectionMatrix();

    this.lastMouseX = newX;
    this.lastMouseY = newY;
  }

  onMouseUp() {
    this.mouseDown = false;
  }

  onKeyUp() {
    this.keyDown = null;
  }

  onKeyDown(event) {
    if (this.mouseDown) {
      return;
    }
    this.keyDown = event.key;
  }

  async componentDidMount() {
    this.canvas = document.getElementById('three-container');
    await this.initializeThree();
    this.bindEvents();
  }

  componentWillUnmount() {
    this.unbindEvents();
  }

  createScene() {
    const scene = new THREE.Scene();
    const annotationScene = new THREE.Scene();

    const axesHelper = new THREE.AxesHelper(5);
    axesHelper.position.y = 3;
    axesHelper.position.x = -6;
    axesHelper.position.z = -3;

    const renderer = new THREE.WebGLRenderer({canvas: this.canvas, preserveDrawingBuffer: true});
    renderer.gammaInput = true;
    renderer.gammaOutput = true;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const camera = new THREE.PerspectiveCamera(75, 800.0 / 600.0, 0.1, 1000);
    camera.position.z = 5;
    camera.position.y = 1;
    camera.rotation.order = 'YXZ';
    camera.updateProjectionMatrix();
    this.camera = camera;

    return {scene, annotationScene, renderer, camera, axesHelper};
  }

  createSceneLights() {
    const ambientLight = new THREE.AmbientLight(0xA0A0A0);
    const strongAmbientLight = new THREE.AmbientLight(0xFFFFFF);

    const spotLight = new THREE.SpotLight(0xA0A0A0);
    spotLight.position.set(2, 4, 6);
    spotLight.intensity = 0.5;
    spotLight.penumbra = 0.05;
    spotLight.decay = 20;
    spotLight.castShadow = true;
    spotLight.shadow.mapSize.width = 1024;
    spotLight.shadow.mapSize.height = 1024;
    spotLight.shadow.camera.near = 0.5;
    spotLight.shadow.camera.far = 200;
    const spotLightHelper = new THREE.SpotLightHelper(spotLight);
    const shadowCameraHelper = new THREE.CameraHelper(spotLight.shadow.camera);
    spotLight.animate = () => {
      spotLight.position.x += spotLight.spotLightIncreasing ? 0.04 : -0.04;
      if (spotLight.position.x >= 10) {
        spotLight.spotLightIncreasing = false;
      } else if (spotLight.position.x <= -1) {
        spotLight.spotLightIncreasing = true;
      }
    };

    const spotLight2 = spotLight.clone();
    spotLight2.position.set(-6, 6, -2);
    spotLight2.animate = () => {
      spotLight2.position.z += spotLight2.spotLightIncreasing ? 0.0192 : -0.0192;
      if (spotLight2.position.z >= 15) {
        spotLight2.spotLightIncreasing = false;
      } else if (spotLight2.position.z <= -1.5) {
        spotLight2.spotLightIncreasing = true;
      }
    };

    return {ambientLight, strongAmbientLight, spotLight, spotLight2, spotLightHelper, shadowCameraHelper};
  }

  createSceneObjects() {
    const cube = new THREE.Mesh(
      new THREE.BoxGeometry(1, 1, 1),
      new THREE.MeshStandardMaterial({color: 0x00ff00})
    );
    cube.position.y = 1;
    cube.castShadow = true;
    cube.animate = () => {
      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;
    };

    const plane = new THREE.Mesh(
      new THREE.PlaneGeometry(200, 200),
      new THREE.MeshPhysicalMaterial({
        reflectivity: 0.0,
        metalness: 0.0,
        roughness: 1.0,
        color: colors.floor[0],
        side: THREE.DoubleSide
      })
    );
    plane.rotation.x = rightAngle;
    plane.rotation.y = 0;
    plane.receiveShadow = true;

    const mainField = this.createField();
    const leftField = this.createField(-courtWidth - courtSpacing);
    const rightField = this.createField(courtWidth + courtSpacing);

    return {cube, plane, mainField, leftField, rightField};
  }

  async loadPerson() {
    return new Promise((res, rej) => {
      this.loader.load(
        '/models/low_poly_person/scene.gltf',
        (result) => res(result),
        () => {},
        (err) => rej(err)
      );
    });
  }

  async getPlayers() {
    const person = await this.loadPerson();
    person.scene.scale.set(0.2, 0.2, 0.2);

    const clone = () => {
      const cloned = person.scene.clone();
      cloned.position.y = -0.47;
      return cloned;
    };

    const mainBottom = clone();
    mainBottom.rotation.y = rightAngle;
    mainBottom.position.z = courtWidth * 0.8;

    const mainTop = clone();
    mainTop.rotation.y = -rightAngle;
    mainTop.position.z = -courtWidth * 0.8;

    const leftBottom = clone();
    leftBottom.position.x = -courtWidth - courtSpacing;
    leftBottom.rotation.y = rightAngle;
    leftBottom.position.z = courtWidth * 0.8;

    const leftTop = clone();
    leftTop.position.x = -courtWidth - courtSpacing;
    leftTop.rotation.y = -rightAngle;
    leftTop.position.z = -courtWidth * 0.8;

    const rightBottom = clone();
    rightBottom.position.x = courtWidth + courtSpacing;
    rightBottom.rotation.y = rightAngle;
    rightBottom.position.z = courtWidth * 0.8;

    const rightTop = clone();
    rightTop.position.x = courtWidth + courtSpacing;
    rightTop.rotation.y = -rightAngle;
    rightTop.position.z = -courtWidth * 0.8;

    const randomizeBottomPositionZ = (player) => {
      player.position.z = (courtHeight / 2.0) * Math.random();
      player.position.z += 0.1;
    };
    const randomizeTopPositionZ = (player) => {
      player.position.z = -(courtHeight / 2.0) * Math.random();
      player.position.z -= 0.1;
    };
    const randomizeBottomRotation = (player) => {
      player.rotation.y = (rightAngle / 2.0) + (rightAngle * Math.random());
    };
    const randomizeTopRotation = (player) => {
      player.rotation.y = -(rightAngle / 2.0) - (rightAngle * Math.random());
    };
    const randomizePositionX = (player, originX) => {
      player.position.x = originX - (courtWidth / 2.0) + (courtWidth * Math.random());
    };

    this.animatePlayers = () => {
      randomizeBottomPositionZ(mainBottom);
      randomizePositionX(mainBottom, 0);
      randomizeBottomRotation(mainBottom);

      randomizeTopPositionZ(mainTop);
      randomizePositionX(mainTop, 0);
      randomizeTopRotation(mainTop);

      randomizeBottomPositionZ(leftBottom);
      randomizePositionX(leftBottom, -courtWidth - courtSpacing);
      randomizeBottomRotation(leftBottom);

      randomizeTopPositionZ(leftTop);
      randomizePositionX(leftTop, -courtWidth - courtSpacing);
      randomizeTopRotation(leftTop);

      randomizeBottomPositionZ(rightBottom);
      randomizePositionX(rightBottom, courtWidth + courtSpacing);
      randomizeBottomRotation(rightBottom);

      randomizeTopPositionZ(rightTop);
      randomizePositionX(rightTop, courtWidth + courtSpacing);
      randomizeTopRotation(rightTop);
    };

    return {mainBottom, mainTop, leftBottom, leftTop, rightBottom, rightTop};
  }

  createField(xOrigin = 0) {
    const parts = [];
    const material = new THREE.MeshPhysicalMaterial({
      reflectivity: 0.0,
      metalness: 0.0,
      roughness: 1.0,
      color: colors.line[0],
      side: THREE.DoubleSide
    });
    const halfWidth = courtWidth / 2.0;
    const halfHeight = courtHeight / 2.0;
    const lineWidth = 0.04;
    const halfLine = lineWidth / 2.0;
    const lineCenterOffset = (initialOffset) => {
      if (initialOffset > 0) {
        return initialOffset - halfLine;
      }
      if (initialOffset < 0) {
        return initialOffset + halfLine;
      }
      return initialOffset;
    };

    const addVertical = (xOffset, zOffset = 0, height = courtHeight) => {
      xOffset = lineCenterOffset(xOffset);
      zOffset = lineCenterOffset(zOffset);
      const part = new THREE.Mesh(new THREE.PlaneGeometry(lineWidth, height), material);
      part.position.x = xOrigin + xOffset;
      part.position.z = zOffset;
      parts.push(part);
    };

    const addHorizontal = (zOffset) => {
      zOffset = lineCenterOffset(zOffset);
      const part = new THREE.Mesh(new THREE.PlaneGeometry(courtWidth, lineWidth), material);
      part.position.x = xOrigin;
      part.position.z = zOffset;
      parts.push(part);
    };

    // long service line for singles
    addHorizontal(halfHeight);
    addHorizontal(-halfHeight);

    // long service line for doubles
    addHorizontal(halfHeight - 0.72);
    addHorizontal(-halfHeight + 0.72);

    // side line for doubles
    addVertical(halfWidth);
    addVertical(-halfWidth);

    // side line for singles
    addVertical(halfWidth - 0.42);
    addVertical(-halfWidth + 0.42);

    // centre line
    const centreLineLength = 4.72;
    const centreLineOffset = 1.98 + (centreLineLength / 2.0);
    addVertical(0, centreLineOffset, centreLineLength);
    addVertical(0, -centreLineOffset, centreLineLength);

    // net line
    addHorizontal(0);

    // short service line
    addHorizontal(1.98);
    addHorizontal(-1.98);

    parts.forEach((part) => {
      part.rotation.x = rightAngle;
      part.rotation.y = 0;
      part.position.y = 0.002;
    });


    const poleHeight = 1.55;
    const poleMaterial = new THREE.MeshPhysicalMaterial({
      reflectivity: 0.0,
      metalness: 0.0,
      roughness: 1.0,
      color: 0x000040,
      side: THREE.DoubleSide
    });

    const leftPole = new THREE.Mesh(new THREE.PlaneGeometry(lineWidth, poleHeight), poleMaterial);
    leftPole.position.y = poleHeight / 2.0;
    leftPole.position.x = xOrigin - halfWidth + halfLine;
    parts.push(leftPole);

    const rightPole = new THREE.Mesh(new THREE.PlaneGeometry(lineWidth, poleHeight), poleMaterial);
    rightPole.position.y = poleHeight / 2.0;
    rightPole.position.x = xOrigin + halfWidth - halfLine;
    parts.push(rightPole);

    const netBand = new THREE.Mesh(new THREE.PlaneGeometry(courtWidth, halfLine), material);
    netBand.position.y = poleHeight;
    netBand.position.x = xOrigin;
    parts.push(netBand);

    const netMaterial = new THREE.MeshPhysicalMaterial({
      reflectivity: 0.0,
      metalness: 0.0,
      roughness: 1.0,
      color: 0xffffff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.45
    });
    const netHeight = 0.76;
    const net = new THREE.Mesh(new THREE.PlaneGeometry(courtWidth, netHeight), netMaterial);
    net.position.x = xOrigin;
    net.position.y = poleHeight - (netHeight / 2.0);
    parts.push(net);

    parts.forEach((part) => {
      part.receiveShadow = true;
      part.castShadow = false;
    });

    const plane = new THREE.Mesh(
      new THREE.PlaneGeometry(courtWidth + (courtHeight * 0.1), courtHeight + (courtHeight * 0.1)),
      new THREE.MeshPhysicalMaterial({
        reflectivity: 0.0,
        metalness: 0.0,
        roughness: 1.0,
        color: colors.court[0],
        side: THREE.DoubleSide
      })
    );
    plane.position.x = xOrigin;
    plane.position.y = 0.001;
    plane.rotation.x = rightAngle;
    plane.receiveShadow = true;
    parts.push(plane);

    return parts;
  }

  createAnnotationField(xOrigin = 0) {
    const annotationPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(courtWidth, courtHeight),
      new THREE.MeshPhysicalMaterial({
        reflectivity: 0.0,
        metalness: 0.0,
        roughness: 1.0,
        color: 0xFFFF00,
        side: THREE.DoubleSide
      })
    );
    annotationPlane.position.x = xOrigin;
    annotationPlane.position.y = 0.003;
    annotationPlane.rotation.x = rightAngle;
    annotationPlane.receiveShadow = false;
    annotationPlane.renderOrder = 9999;
    return annotationPlane;
  }

  async initializeThree() {
    const {scene, annotationScene, renderer, camera, axesHelper} = this.createScene();
    const {ambientLight, strongAmbientLight, spotLight, spotLight2, spotLightHelper, shadowCameraHelper} = this.createSceneLights();
    const {cube, plane, mainField, leftField, rightField} = this.createSceneObjects();
    const players = await this.getPlayers();

    // scene.add(axesHelper);
    scene.add(ambientLight);
    scene.add(spotLight);
    scene.add(spotLight2);
    mainField.forEach((fieldPart) => scene.add(fieldPart));
    leftField.forEach((fieldPart) => scene.add(fieldPart));
    rightField.forEach((fieldPart) => scene.add(fieldPart));
    // scene.add(spotLightHelper);
    // scene.add(shadowCameraHelper);

    // scene.add(cube);
    scene.add(plane);

    Object.values(players).forEach((player) => scene.add(player));

    annotationScene.add(this.createAnnotationField(0));
    annotationScene.add(this.createAnnotationField(-courtWidth - courtSpacing));
    annotationScene.add(this.createAnnotationField(courtWidth + courtSpacing));
    annotationScene.add(strongAmbientLight.clone());

    this.animateColors = () => {
      plane.material.color.setHex(colors.random(colors.floor));

      leftField[0].material.color.setHex(colors.random(colors.line));
      mainField[0].material.color.setHex(colors.random(colors.line));
      rightField[0].material.color.setHex(colors.random(colors.line));

      leftField[17].material.color.setHex(colors.random(colors.court));
      mainField[17].material.color.setHex(colors.random(colors.court));
      rightField[17].material.color.setHex(colors.random(colors.court));
    };

    renderer.autoClear = false;
    const animate = () => {
      requestAnimationFrame(animate);
      cube.animate();
      spotLight.animate();
      spotLight2.animate();
      this.handleMovement();
      renderer.clear();
      renderer.render(scene, camera);
      if (this.renderAnnotations) {
        renderer.clearDepth();
        renderer.render(annotationScene, camera);
      }
    };
    animate();
  }

  handleMovement() {
    if (!this.keyDown) {
      return;
    }
    const baseSpeed = 0.1;
    let forwardSpeed = 0;
    let strafeSpeed = 0;
    let jumpSpeed = 0;
    if (this.keyDown === 'w') {
      forwardSpeed = baseSpeed;
    } else if (this.keyDown === 'a') {
      strafeSpeed = baseSpeed;
    } else if (this.keyDown === 's') {
      forwardSpeed = -baseSpeed;
    } else if (this.keyDown === 'd') {
      strafeSpeed = -baseSpeed;
    } else if (this.keyDown === 'q') {
      jumpSpeed = baseSpeed;
    } else if (this.keyDown === 'e') {
      jumpSpeed = -baseSpeed;
    } else if (this.keyDown === 'r' && this.animatePlayers) {
      this.animatePlayers();
      this.animateColors();
      this.keyDown = null;
    } else if (this.keyDown === 'n') {
      this.renderAnnotations = !this.renderAnnotations;
      this.keyDown = null;
    } else if (this.keyDown === 'j') {
      canvasToImage('three-container', {type: 'jpg'});
      this.keyDown = null;
    }

    const yaw = this.camera.rotation.y;
    const pitch = this.camera.rotation.x;

    this.camera.position.x -= Math.sin(yaw) * forwardSpeed;
    this.camera.position.z -= Math.cos(yaw) * Math.cos(pitch) * forwardSpeed;
    this.camera.position.y += Math.sin(pitch) * forwardSpeed;

    this.camera.position.x -= Math.cos(yaw) * strafeSpeed;
    this.camera.position.z += Math.sin(yaw) * strafeSpeed;

    this.camera.position.x -= Math.sin(yaw) * Math.sin(pitch) * jumpSpeed;
    this.camera.position.y -= Math.cos(pitch) * jumpSpeed;
    this.camera.position.z -= Math.sin(pitch) * Math.cos(yaw) * jumpSpeed;
  }

  render() {
    return (
      <div>
        <div className='content' style={{marginBottom: '40px'}}>
          <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly'}}>
            <CourtInstructionView/>
            <Paper style={{paddingTop: '50px', paddingBottom: '50px', width: '900px'}}>
              <canvas id='three-container' width='800px' height='600px'></canvas>
            </Paper>
          </div>
        </div>
      </div>
    );
  }
}
