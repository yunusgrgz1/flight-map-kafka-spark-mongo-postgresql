// 🌍 Harita başlat
const map = L.map('map').setView([39.0, 35.0], 5);

// 🗺️ Harita katmanı
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// 🛩️ Uçak ikonunu yönlendirecek fonksiyon
function getAirplaneIcon(direction) {
  const iconUrl = 'images/airplane.svg';  // SVG dosyanızın yolu

  // SVG'yi yönüne göre döndürme
  const icon = L.divIcon({
    className: 'airplane-icon',  // Icon'un sınıf adı
    html: `<img src="${iconUrl}" style="transform: rotate(${direction - 90}deg);" width="20" height="20" />`,  // Yönü döndüren CSS
    iconSize: [32, 32],  // Boyut
    iconAnchor: [16, 16],  // Orta nokta
    popupAnchor: [0, -10]  // Popup yeri
  });

  return icon;
}

// ✈️ Marker'lar
const flightMarkers = {};

// 🔄 API'den verileri çek
async function fetchFlights() {
  try {
    const response = await fetch("http://localhost:5000/api/flights");
    const data = await response.json();

    data.flights.forEach(flight => {
      const id = flight.flight_id;
      const lat = flight.current_location.latitude;
      const lon = flight.current_location.longitude;
      const direction = flight.direction;  // API'den gelen uçuş yönü
      const info = `
        <b>${flight.airline}</b><br>
        ${flight.departure_city} ➡️ ${flight.arrival_city}<br>
        Speed: ${flight.current_speed_km_h} km/h<br>
        Altitude: ${flight.current_altitude_m} m
      `;

      // Eğer marker varsa güncelle
      if (flightMarkers[id]) {
        flightMarkers[id]
          .setLatLng([lat, lon])  // Konumu güncelle
          .setPopupContent(info);  // Popup içeriğini güncelle
      } else {
        // Yeni marker ekle
        const marker = L.marker([lat, lon], { 
          icon: getAirplaneIcon(direction)  // Yönüne göre dönen SVG ikon
        }).addTo(map).bindPopup(info);

        flightMarkers[id] = marker;
      }
    });

  } catch (error) {
    console.error("Veri çekme hatası:", error);
  }
}

// ⏱ Başlat
fetchFlights();
setInterval(fetchFlights, 5000);  // Her 5 saniyede bir güncelle
