import React, { useState } from 'react';
import AddTask from './AddTask';
import './tempelates/TaskList.css';

function Task({ task, onDelete, onAdd, onToggleCompletion, onUpdateContent, getUncles, onMoveTask }) {
    const [isEditing, setIsEditing] = useState(false);
    const [editedContent, setEditedContent] = useState(task.content);
    const [isCollapsed, setIsCollapsed] = useState(false);

    const toggleCollapse = () => {
        setIsCollapsed(!isCollapsed);
    };

    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this task?")) {
            onDelete(task.id);
        }
    };

    const handleEdit = () => {
        setIsEditing(!isEditing);
        if (isEditing) {
            onUpdateContent(task.id, editedContent);
        }
    };

    const handleCompletionToggle = () => {
        onToggleCompletion(task.id);
    };

    const handleMoveTo = (newParentId) => {
        onMoveTask(task.id, newParentId);
    };

    const uncles = getUncles(task.id);

    const taskStyle = task.parentId ? {} : { fontWeight: 'bold' };

    return (
        <div className="task-container">
            <div className="task-header">
                {task.sub_items && task.sub_items.length > 0 && (
                    <span 
                        className={`collapsible-icon ${isCollapsed ? 'collapsed' : ''}`} 
                        onClick={toggleCollapse}
                    >▶</span>
                )}
                {isEditing ? (
                    <input
                        value={editedContent}
                        onChange={(e) => setEditedContent(e.target.value)}
                        style={taskStyle}
                        className={`task-input ${task.is_completed ? 'completed' : ''}`}
                    />
                ) : (
                    <p style={taskStyle} className={`task-text ${task.is_completed ? 'completed' : ''}`}>{task.content}</p>
                )}
                <input
                    type="checkbox"
                    checked={task.is_completed}
                    onChange={handleCompletionToggle}
                    className="task-completion-checkbox"
                />
            </div>
    
            <div className="task-controls">
                <div className="buttons-container">
                    <button className="delete" onClick={handleDelete}></button>
                    <button className="edit" onClick={handleEdit}></button>
                </div>
                <AddTask onAdd={onAdd} parentId={task.id} />
                {uncles && uncles.length > 0 && (
                    <select defaultValue="default" onChange={(e) => handleMoveTo(Number(e.target.value))}>
                        <option value="default" disabled>Move to...</option>
                        {uncles.map(uncle => (
                            <option key={uncle.id} value={uncle.id}>
                                {uncle.content}
                            </option>
                        ))}
                    </select>
                )}
            </div>
    
            {!isCollapsed && task.sub_items && task.sub_items.length > 0 && (
                <div className="subtask">
                    <TasksList 
                        tasks={task.sub_items} 
                        onDelete={onDelete} 
                        onAdd={onAdd} 
                        onToggleCompletion={onToggleCompletion} 
                        onUpdateContent={onUpdateContent} 
                        getUncles={getUncles} 
                        onMoveTask={onMoveTask} 
                    />
                </div>
            )}
        </div>
    );
}

function TasksList({ tasks, onDelete, onAdd, onToggleCompletion, onUpdateContent, getUncles, onMoveTask }) {
    return (
        <div className="tasks-list">
            {tasks.map(task => (
                <Task 
                    key={task.id} 
                    task={task} 
                    onDelete={onDelete} 
                    onAdd={onAdd} 
                    onToggleCompletion={onToggleCompletion} 
                    onUpdateContent={onUpdateContent}
                    getUncles={getUncles} 
                    onMoveTask={onMoveTask}
                />
            ))}
        </div>
    );
}

export default TasksList;