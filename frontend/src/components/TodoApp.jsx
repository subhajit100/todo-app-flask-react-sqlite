import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [form, setForm] = useState({ title: '', description: '' });

  const API_URL = 'http://127.0.0.1:5000/api/todos';

  // Fetch Todos
  useEffect(() => {
    axios.get(API_URL)
      .then(response => setTodos(response.data))
      .catch(error => console.error('Error fetching todos:', error));
  }, []);

  // Add Todo
  const addTodo = () => {
    axios.post(API_URL, form)
      .then(response => setTodos([...todos, response.data]))
      .catch(error => console.error('Error adding todo:', error));
  };

  // Update Todo
  const updateTodo = (id) => {
    const updatedTitle = prompt('Enter new title:', '');
    const updatedDescription = prompt('Enter new description:', '');
    axios.put(`${API_URL}/${id}`, { title: updatedTitle, description: updatedDescription })
      .then(response => {
        setTodos(todos.map(todo => (todo.id === id ? response.data : todo)));
      })
      .catch(error => console.error('Error updating todo:', error));
  };

  // Delete Todo
  const deleteTodo = (id) => {
    axios.delete(`${API_URL}/${id}`)
      .then(() => setTodos(todos.filter(todo => todo.id !== id)))
      .catch(error => console.error('Error deleting todo:', error));
  };

  return (
    <div className="App">
      <h1>Todo App</h1>
      <div>
        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <button onClick={addTodo}>Add Todo</button>
      </div>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <h3>{todo.title}</h3>
            <p>{todo.description}</p>
            <button onClick={() => updateTodo(todo.id)}>Update</button>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoApp;
