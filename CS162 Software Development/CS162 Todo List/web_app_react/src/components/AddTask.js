import React, { useState } from 'react';

function AddTask({ onAdd, parentId = null }) {
    const [content, setContent] = useState('');
  
    const handleSubmit = (e) => {
      e.preventDefault();
      if (content.trim()) {
        onAdd(content, parentId);
        setContent('');
      }
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Add task..." 
          value={content}
          onChange={(e) => setContent(e.target.value)} 
        />
        <button type="submit">+</button>
      </form>
    );
  }
  
  export default AddTask;