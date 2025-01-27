import "./App.css";
import { SearchBar } from "./components/SearchBar";

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <SearchBar />
      </header>
    </div>
  );
};

export default App;
