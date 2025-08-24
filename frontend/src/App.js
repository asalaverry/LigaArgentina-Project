import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Equipos from "./pages/Equipos";
import EquipoDetalle from "./pages/EquipoDetalle";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Equipos />} />
        <Route path="/equipo/:id" element={<EquipoDetalle />} />
      </Routes>
    </Router>
  );
}

export default App;
