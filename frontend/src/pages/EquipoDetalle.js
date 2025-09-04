import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./EquipoDetalle.css";

//Para agregar las flags en jugadores
import Flag from "react-world-flags";
import { getISOCode } from "./utils/flags"; 

function EquipoDetalle() {
  const { id } = useParams(); // Obtiene el ID del equipo desde la URL
  const [equipo, setEquipo] = useState(null); // Crea una variable de estado para el equipo
  const [posicionActiva, setPosicionActiva] = useState("Arqueros"); // Gestiona la pestaña activa
  const navigate = useNavigate(); // Funcion para navegar a otras rutas. Lo usa el boton home

  useEffect(() => { // Obtiene los datos de la API
    fetch(`http://127.0.0.1:5000/equipos/${id}`)
      .then(res => res.json())
      .then(data => setEquipo(data));
  }, [id]);

  useEffect(() => { // Actualiza el título de la página, al equipo que se este viendo
  if (equipo && equipo.equipo && equipo.equipo.nombre) {
    document.title = equipo.equipo.nombre;
  } else {
    document.title = "Liga Argentina Viewer";
  }
}, [equipo]);

  if (!equipo) return <div>Cargando...</div>; // Muestra un mensaje de carga mientras se obtienen los datos

  // Define las posiciones posibles de los jugadores
  const jugadoresPorPosicion = {
    Arqueros: [],
    Defensores: [],
    Mediocampistas: [],
    Delanteros: [],
  };

  equipo.jugadores.forEach(j => { // Clasifica los jugadores en sus respectivas posiciones
    if (j.posicion.includes("Arq")) jugadoresPorPosicion.Arqueros.push(j);
    else if (j.posicion.includes("Def")) jugadoresPorPosicion.Defensores.push(j);
    else if (j.posicion.includes("Med")) jugadoresPorPosicion.Mediocampistas.push(j);
    else if (j.posicion.includes("Del")) jugadoresPorPosicion.Delanteros.push(j);
  });


  return (
    <div className="detalle-container fade-in">

      {/* Botón Home: Regresar a la página principal */}
      <button className="btn-home" onClick={() => navigate("/")}>
        <img src="/home.png" alt="Home" />
      </button>

      {/* HEADER: Datos principales del equipo */}
      <div className="detalle-header">
        <img src={equipo.equipo.logo} alt={equipo.equipo.nombre_completo} className="detalle-logo" />
        <div className="detalle-info">
          <h1 className="detalle-nombre">{equipo.equipo.nombre_completo}</h1>
          <h2 className="detalle-estadio">Estadio: {equipo.equipo.estadio}</h2>
        </div>
      </div>

      <hr className="detalle-separador" />

      {/* JUGADORES */}
      <div className="jugadores-seccion">
        <h2 className="jugadores-titulo-principal">Jugadores</h2>

        {/* TABS: Cada seccion de jugadores por posicion */}
        <div className="tabs">
          {Object.keys(jugadoresPorPosicion).map(pos => (
            <button
              key={pos}
              className={`tab ${posicionActiva === pos ? "activo" : ""}`}
              onClick={() => setPosicionActiva(pos)}
 >
              {pos}
            </button>
          ))}
        </div>

        {/* CONTENIDO: El contenido de cada TAB --> Los jugadores de esa posicion */}
        <div key={posicionActiva} className="jugadores-grupo fade-in">
          <div className="jugadores-lista">
            {jugadoresPorPosicion[posicionActiva].map(j => (
              <div key={j.id} className="jugador-item">
                <span className="jugador-nombre">{j.nombre}</span>
                <span className="jugador-numero">#{j.numero || "N/A"}</span> {/* Algunos jugadores no tienen numero, y se muestra "N/A" */}
                <span className="jugador-info">
                  {j.edad} años
                  {getISOCode(j.nacionalidad) && (
                    <Flag code={getISOCode(j.nacionalidad)} className="flag" /> // Muestra la bandera si se encuentra el codigo ISO de la nacionalidad
                  )}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default EquipoDetalle;
