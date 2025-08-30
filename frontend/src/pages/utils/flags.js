const nacionalidadToISO = {
    "Argentina": "AR",
    "Paraguay": "PY",
    "Ecuador": "EC",
    "Uruguay": "UY",
    "Colombia": "CO",
    "Siria": "SY",
    "Japón": "JP",
    "Italia": "IT",
    "Perú": "PE",
    "Armenia": "AM",
    "Suiza": "CH",
    "Chile": "CL",
    "España": "ES",
    "Brasil": "BR",
    "Venezuela": "VE",
    "México": "MX",
    "Estados Unidos": "US",
    "Eslovenia": "SI",
    "Malasia": "MY"
};

export function getISOCode(nacionalidad) {
  return nacionalidadToISO[nacionalidad] || null;
}