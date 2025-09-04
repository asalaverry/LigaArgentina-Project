// BrowserRouter es el router principal que permite el enrutamiento del lado del cliente
// Routes es el contenedor que define las rutas de la aplicación.
// Route es el componente individual que asocia una URL con un componente.
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
 
import Equipos from "./pages/Equipos";
import EquipoDetalle from "./pages/EquipoDetalle";

function App() {
  return (
    // Envuelve toda la aplicacion en el router para habilitar la navegacion entre paginas
    <Router>
      <Routes>
        {/* Define las rutas de la aplicacion */}
        <Route path="/" element={<Equipos />} />
        <Route path="/equipo/:id" element={<EquipoDetalle />} />
      </Routes>
    </Router>
  );
}

export default App;
