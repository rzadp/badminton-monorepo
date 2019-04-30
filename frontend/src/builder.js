import {EventEmitter} from 'events';
import Model from './services/model';
import modelJson from '../static/models/model.json';
import weightsBin from '../static/models/weights.bin';

export default class Builder {
  static async build() {
    const events = new EventEmitter();
    const model = new Model();
    await model.load(modelJson, weightsBin);

    const services = {
      events,
      model
    };

    return services;
  }
}
