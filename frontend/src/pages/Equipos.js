import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Equipos.css"; // Importamos estilos
import { motion } from "framer-motion"; // 👈 import

function Equipos() {
  const [equipos, setEquipos] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/equipos")
      .then(res => res.json())
      .then(data => setEquipos(data.equipos));
  }, []);

  return (
    <div className="equipos-container">
      {equipos.map((e, i) => (
        <motion.div
          key={e.id}
          initial={{ opacity: 0, y: 40 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ duration: 0.5, delay: i * 0.05 }} 
        >
          <Link to={`/equipo/${e.id}`} className="equipo-card">
            <img src={e.logo} alt={e.nombre} className="equipo-logo" />
            <div className="equipo-nombre">{e.nombre}</div>
          </Link>
        </motion.div>
      ))}
    </div>
  );
}

export default Equipos;

