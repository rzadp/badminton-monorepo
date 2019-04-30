import * as tf from '@tensorflow/tfjs';

export default class Model {
  async load(modelJson, weightsBin) {
    this.modelJson = modelJson;
    this.weightsBin = weightsBin;

    const loadedModel = await tf.loadModel('static/models/model.json');
    this.loadedModel = loadedModel;
  }

  predict(image) {
    const xs = tf.tensor4d(
      image,
      [1, 28, 28, 1]);

    const output = this.loadedModel.predict(xs);
    const axis = 1;
    const predictions = Array.from(output.argMax(axis).dataSync());
    return predictions[0];
  }
}
