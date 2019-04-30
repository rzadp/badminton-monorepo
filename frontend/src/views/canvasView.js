import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';

export default class CanvasView extends Component {
  static propTypes = {
    onPredict: PropTypes.func,
    onClear: PropTypes.func
  };

  constructor(props) {
    super(props);
    this.handlePredict = this.handlePredict.bind(this);
    this.handleClear = this.handleClear.bind(this);
  }

  componentDidMount() {
    this.initializeCanvas();
  }

  initializeCanvas() {
    this.canvas = document.getElementById('mycanvas');
    const context = this.canvas.getContext('2d');
    context.lineWidth = 13;
    this.canvas.onmousedown = (e) => {
      const pos = this.fixPosition(e, this.canvas);
      this.mousedown = true;
      context.beginPath();
      context.moveTo(pos.x, pos.y);
      return false;
    };

    this.canvas.onmousemove = (e) => {
      const pos = this.fixPosition(e, this.canvas);
      if (this.mousedown) {
        context.lineTo(pos.x, pos.y);
        context.stroke();
      }
    };

    this.canvas.onmouseup = () => this.mousedown = false;
  }

  fixPosition(e, gCanvasElement) {
    let x;
    let y;
    if (e.pageX || e.pageY) {
      x = e.pageX;
      y = e.pageY;
    } else {
      x = e.clientX + document.body.scrollLeft +
          document.documentElement.scrollLeft;
      y = e.clientY + document.body.scrollTop +
          document.documentElement.scrollTop;
    }
    x -= gCanvasElement.offsetLeft;
    y -= gCanvasElement.offsetTop;
    return {x, y};
  }

  async handlePredict() {
    const bigImageData = this.canvas.getContext('2d').getImageData(0, 0, this.canvas.width, this.canvas.height);
    const bitmap = await createImageBitmap(bigImageData, 0, 0, this.canvas.width, this.canvas.height);

    const resizedCanvas = document.createElement('canvas');
    const resizedContext = resizedCanvas.getContext('2d');
    resizedCanvas.width = 28;
    resizedCanvas.height = 28;
    resizedContext.drawImage(bitmap, 0, 0, this.canvas.width, this.canvas.height, 0, 0, 28, 28);

    const resizedImageData = resizedContext.getImageData(0, 0, resizedCanvas.width, resizedCanvas.height);
    const finalImage = new Float32Array(28 * 28);

    for (let j = 0; j < resizedImageData.data.length / 4; j++) {
      finalImage[j] = resizedImageData.data[(j * 4) + 3] / 255.0;
    }

    this.props.onPredict(finalImage);
  }

  handleClear() {
    this.mousedown = false;
    this.canvas.getContext('2d').clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.props.onClear();
  }

  render() {
    const buttonStyle = {marginLeft: '15px', marginRight: '15px'};

    return (
      <Paper style={{padding: '30px', display: 'inline-block'}}>
        <div>~ Obszar do rysowania cyfr ~</div>
        <canvas width={280} height={280} id="mycanvas" style={{border: '1px solid blue', marginTop: '15px'}}/>
        <div style={{marginTop: '20px'}}>
          <Button style={buttonStyle} color="primary" variant="contained" onClick={this.handlePredict}>Predict</Button>
          <Button style={buttonStyle}  color="secondary" variant="contained" onClick={this.handleClear}>Clear</Button>
        </div>

      </Paper>
    );
  }
}
