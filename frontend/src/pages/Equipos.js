import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Equipos.css"; // Importamos estilos
import { motion } from "framer-motion"; // Importamos framer-motion para animaciones

function Equipos() {
  const [equipos, setEquipos] = useState([]); // Crea var de estado para almacenar los equipos

  useEffect(() => {
    document.title = "Liga Argentina Viewer"; // Cambia el titulo de la pagina
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/equipos") // Peticion a la URL para obtener los equipos
      .then(res => res.json()) // Convierte la respuesta (la respuesta al fetch) a JSON
      .then(data => { // Aca procesa los datos
        setTimeout(() => {
          setEquipos(data.equipos); // Actualiza el estado con los equipos obtenidos
        }, 500); // 500ms de delay
      });
  }, []);

  return (
    <div className="equipos-container">
      {equipos.map((e, i) => ( // equipos.map itera sobre el array de equipos y renderiza una tarjeta 
        <motion.div // Componente de framer-motion para animaciones
          key={e.id}
          initial={{ opacity: 0, y: 40 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ duration: 0.5, delay: i * 0.05 }} 
        >
          <Link to={`/equipo/${e.id}`} className="equipo-card"> {/* Crea el enlace a la pagina de detalle del equipo */}
            <img src={e.logo} alt={e.nombre} className="equipo-logo" />
            <div className="equipo-nombre">{e.nombre}</div>
          </Link>
        </motion.div>
      ))}
    </div>
  );
}

export default Equipos;

