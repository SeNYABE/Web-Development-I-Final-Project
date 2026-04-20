const races = [
  { raceId: 1, name: "Australian Grand Prix", date: "2026-03-08", location: "Melbourne" },
  { raceId: 2, name: "Chinese Grand Prix", date: "2026-03-15", location: "Shanghai", sprint: true },
  { raceId: 3, name: "Japanese Grand Prix", date: "2026-03-29", location: "Suzuka" },
  { raceId: 4, name: "Miami Grand Prix", date: "2026-05-03", location: "Miami", sprint: true },
  { raceId: 5, name: "Canadian Grand Prix", date: "2026-05-24", location: "Montreal", sprint: true },
  { raceId: 6, name: "Monaco Grand Prix", date: "2026-06-07", location: "Monaco" },
  { raceId: 7, name: "Barcelona-Catalunya Grand Prix", date: "2026-06-14", location: "Barcelona" },
  { raceId: 8, name: "Austrian Grand Prix", date: "2026-06-28", location: "Spielberg" },
  { raceId: 9, name: "British Grand Prix", date: "2026-07-05", location: "Silverstone", sprint: true },
  { raceId: 10, name: "Belgian Grand Prix", date: "2026-07-19", location: "Spa-Francorchamps" },
  { raceId: 11, name: "Hungarian Grand Prix", date: "2026-07-26", location: "Budapest" },
  { raceId: 12, name: "Dutch Grand Prix", date: "2026-08-23", location: "Zandvoort", sprint: true },
  { raceId: 13, name: "Italian Grand Prix", date: "2026-09-06", location: "Monza" },
  { raceId: 14, name: "Spanish Grand Prix", date: "2026-09-14", location: "Madrid" },
  { raceId: 15, name: "Azerbaijan Grand Prix", date: "2026-09-26", location: "Baku" },
  { raceId: 16, name: "Singapore Grand Prix", date: "2026-10-11", location: "Marina Bay", sprint: true },
  { raceId: 17, name: "United States Grand Prix", date: "2026-10-25", location: "Austin" },
  { raceId: 18, name: "Mexico City Grand Prix", date: "2026-11-01", location: "Mexico City" },
  { raceId: 19, name: "Sao Paulo Grand Prix", date: "2026-11-08", location: "Sao Paulo" },
  { raceId: 20, name: "Las Vegas Grand Prix", date: "2026-11-21", location: "Las Vegas" },
  { raceId: 21, name: "Qatar Grand Prix", date: "2026-11-29", location: "Lusail" },
  { raceId: 22, name: "Abu Dhabi Grand Prix", date: "2026-12-06", location: "Yas Marina" },
];

const today = new Date();
today.setHours(0, 0, 0, 0); // normalize to start of day

const upcoming_races = {};

races.forEach(race => {
  const raceDate = new Date(race.date);

  if (raceDate >= today) {
    upcoming_races[race.raceId] = race;
    
  }
});

console.log("Upcoming races:", upcoming_races);