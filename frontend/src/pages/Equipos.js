import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Equipos.css"; // Importamos estilos

function Equipos() {
  const [equipos, setEquipos] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/equipos")
      .then(res => res.json())
      .then(data => setEquipos(data.equipos));
  }, []);

  return (
    <div className="equipos-container">
      {equipos.map(e => (
        <Link to={`/equipo/${e.id}`} key={e.id} className="equipo-card">
          <img src={e.logo} alt={e.nombre} className="equipo-logo" />
          <h3 className="equipo-nombre">{e.nombre}</h3>
        </Link>
      ))}
    </div>
  );
}

export default Equipos;

