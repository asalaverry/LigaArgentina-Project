import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function EquipoDetalle() {
  const { id } = useParams();
  const [equipo, setEquipo] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/equipos/${id}`)
      .then(res => res.json())
      .then(data => setEquipo(data));
  }, [id]);

  if (!equipo) return <p>Cargando...</p>;

  // Agrupar jugadores por posición
  const jugadoresPorPosicion = equipo.jugadores.reduce((acc, j) => {
    acc[j.posicion] = acc[j.posicion] || [];
    acc[j.posicion].push(j);
    return acc;
  }, {});

  return (
    <div>
      <h1>{equipo.equipo.nombre}</h1>
      <img src={equipo.equipo.logo} alt={equipo.equipo.nombre} width="100" />
      <p>Estadio: {equipo.equipo.estadio}</p>
      <h2>Jugadores</h2>
      {Object.entries(jugadoresPorPosicion).map(([posicion, jugadores]) => (
        <div key={posicion}>
          <h3>{posicion}</h3>
          <ul>
            {jugadores.map((j, i) => (
              <li key={i}>
                {j.nombre} ({j.nacionalidad}) - #{j.numero}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default EquipoDetalle;
