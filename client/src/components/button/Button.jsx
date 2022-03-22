import React from 'react';
import PropTypes from 'prop-types';

import './button.scss';
import AddBoxOutlinedIcon from '@material-ui/icons/AddBoxOutlined';

const Button = props => {
    return (
        <button
            className={`btn ${props.className}`}
            onClick={props.onClick ? () => props.onClick() : null}
        ><AddBoxOutlinedIcon/>
            {props.children}

        </button>
    );
}

export const OutlineButton = props => {
    return (
        <Button
            className={`btn-outline ${props.className}`}
            onClick={props.onClick ? () => props.onClick() : null}
        >
            {props.children}
        </Button>
    );
}

Button.propTypes = {
    onClick: PropTypes.func
}

export default Button;
