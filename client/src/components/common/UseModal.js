import { useState } from 'react';

const UseModal = () => {
  const [visible, setVisible] = useState(false);
  function toggle() {
    setVisible(!visible);    
  }
  return {toggle, visible}
};

export default UseModal;