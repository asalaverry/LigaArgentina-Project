import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./EquipoDetalle.css";

function EquipoDetalle() {
  const { id } = useParams();
  const [equipo, setEquipo] = useState(null);
  const [posicionActiva, setPosicionActiva] = useState("Arqueros"); // pestaña activa
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/equipos/${id}`)
      .then(res => res.json())
      .then(data => setEquipo(data));
  }, [id]);

  if (!equipo) return <div>Cargando...</div>;

  // Agrupar jugadores por posición
  const jugadoresPorPosicion = {
    Arqueros: [],
    Defensores: [],
    Mediocampistas: [],
    Delanteros: [],
  };

  equipo.jugadores.forEach(j => {
    if (j.posicion.includes("Arq")) jugadoresPorPosicion.Arqueros.push(j);
    else if (j.posicion.includes("Def")) jugadoresPorPosicion.Defensores.push(j);
    else if (j.posicion.includes("Med")) jugadoresPorPosicion.Mediocampistas.push(j);
    else if (j.posicion.includes("Del")) jugadoresPorPosicion.Delanteros.push(j);
  });

  return (
    <div className="detalle-container">
      
      {/* Botón Home arriba a la derecha */}
      <button className="btn-home" onClick={() => navigate("/")}>
        <img src="/home.png" alt="Home" />
      </button>

      {/* HEADER */}
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

        {/* TABS */}
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

        {/* CONTENIDO */}
        <div className="jugadores-grupo">
          <div className="jugadores-lista">
            {jugadoresPorPosicion[posicionActiva].map(j => (
              <div key={j.id} className="jugador-item">
                <span className="jugador-nombre">{j.nombre}</span>
                <span className="jugador-numero">#{j.numero}</span>
                <span className="jugador-info">
                  {j.edad} años, {j.nacionalidad}
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
