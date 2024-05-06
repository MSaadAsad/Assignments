  import React, { useState } from 'react';

  function AddList({ onAdd }) {
    const [content, setContent] = useState('');
  
    const handleSubmit = (e) => {
      e.preventDefault();
      if (content.trim()) {
        onAdd(content);
        setContent('');
      }
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <input
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Add a new list"
        />
        <button type="submit">+</button>
      </form>
    );
  }
  
  export default AddList;