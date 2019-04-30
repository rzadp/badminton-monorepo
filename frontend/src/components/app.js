import React, {Component} from 'react';
import PropTypes from 'prop-types';
import AppBarView from 'views/appBarView';
import Digits from 'components/digits';
import Court from 'components/court';

export default class App extends Component {
  static propTypes = {
    services: PropTypes.object
  };

  constructor(props) {
    super(props);
    this.state = {
      page: 'court',
      result: ''
    };
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

  render() {
    return (
      <div>
        <AppBarView selectedPage={this.state.page} onPageSelected={(page) => this.setState({page})}/>
        {this.state.page === 'digits' && <Digits services={this.props.services}/>}
        {this.state.page === 'court' && <Court services={this.props.services}/>}
      </div>
    );
  }
}
