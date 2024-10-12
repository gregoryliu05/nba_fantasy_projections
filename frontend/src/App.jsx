import { useEffect, useState } from 'react'
import playerService from './services/forms'
import './App.css'


const Table = (props) => {
  const {players} = props

  if (!players) {
    return (
      <table>
      <thead>
        <tr>
          <th>Player</th>
          <th>Overall Score
            <button onClick = {() => {console.log("lol")}}> </button>
          </th>
          <th>Average Fantasy Points 2024</th>
          <th>Projected Fantasy Points 2025</th>
          <th>Consistency</th>
          <th>Injury Risk</th>
          <th>Consistency and Injury Risk</th>
          <th>Position</th>
        </tr>
      </thead>
      <tbody>
      <tr> 
        <td> Loading Table...</td>
      </tr>
      </tbody>
      </table>
    )
  } else {
    return (
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Overall Score</th>
            <th>Average Fantasy Points 2024</th>
            <th>Projected Fantasy Points 2025</th>
            <th>Consistency</th>
            <th>Injury Risk</th>
            <th>Consistency and Injury Risk</th>
            <th>Position</th>
          </tr>
        </thead>
        <tbody>
       {players.map((player, index) => (
          <tr key = {index}>
            <td>{index+1}</td>
            <td> {player.player}</td>
            <td> {player.overallScore}</td>
            <td> {player.averageFPTS}</td>
            <td> {player.projectedFPTS}</td>
            <td> {player.consistency}</td>
            <td> {player.injuryRisk}</td>
            <td> {player.consistencyInjuryRisk}</td>
            <td> {player.position}</td>
          </tr>
        ))}
        </tbody>
      </table>
    )
  }
  
}



const  App = () => {
  const [players, setPlayers] = useState(null)
  const [sortByCategory, setSortByCategory] = useState(0)
  const [sortAscDesc, setSortAscDesc] = useState(false)

  useEffect(() => {
    playerService.getAll().then((response) => {
      console.log(response.data.players)
      setPlayers(response.data.players)
    })
  },[])

  useEffect(() => {
    setPlayers(filteredPlayers)
    console.log(sortByCategory)
  },[sortByCategory, sortAscDesc])


  const handleClick = (int) => {
    setSortByCategory(int); // Sort by Overall Score
    setSortAscDesc(!sortAscDesc); // Toggle between ascending/descending
    console.log(sortAscDesc)
  };
  
  const filteredPlayersAsc = (players) => {
    switch (sortByCategory) {
      case 0: 
        return players.sort((a,b) => b.player.localeCompare(a.player));
      case 1:
        return players.sort((a,b)=> b.overallScore -a.overallScore);
      case 2:
        return players.sort((a,b) => b.averageFPTS - a.averageFPTS);
      case 3: 
        return players.sort((a,b) => b.projectedFPTS - a.projectedFPTS);
      case 4: 
        return players.sort((a,b) => b.consistency - a.consistency);
      case 5: 
        return players.sort((a,b) => b.injuryRisk - a.injuryRisk);
      case 6:
        return players.sort((a,b) => b.consistencyInjuryRisk - a.consistencyInjuryRisk);
      default:
        return players;
    }
  }
  const filteredPlayersDesc = (players) => {
    switch (sortByCategory) {
      case 0: 
        return players.sort((a,b) => a.player.localeCompare(b.player));
      case 1:
        return players.sort((a,b)=> a.overallScore -b.overallScore);
      case 2:
        return players.sort((a,b) => a.averageFPTS - b.averageFPTS);
      case 3: 
        return players.sort((a,b) => a.projectedFPTS - b.projectedFPTS);
      case 4: 
        return players.sort((a,b) => a.consistency - b.consistency);
      case 5: 
        return players.sort((a,b) => a.injuryRisk - b.injuryRisk);
      case 6:
        return players.sort((a,b) => a.consistencyInjuryRisk - b.consistencyInjuryRisk);
      default:
          return players;
    }
  }
  const filteredPlayers= (players) ? ((sortAscDesc)? filteredPlayersAsc(players) : filteredPlayersDesc(players)): players
  
  
  return (
      <>
        <p> Fantasy Projections Rankings</p>
        <header>
        <button onClick = {() => handleClick(0)}> Sort By Name</button>
        <button onClick = {() => handleClick(1)}> Sort By Overall Score</button>
        <button onClick = {() => handleClick(2)}> Sort By Avg Fantasy Points</button>
        <button onClick = {() => handleClick(3)}> Sort By Projected Fantasy Points</button>
        <button onClick = {() => handleClick(4)}> Sort By Consistency</button>
        <button onClick = {() => handleClick(5)}> Sort By Injury Risk</button>
        <button onClick = {() => handleClick(6)}> Sort By C+ IR</button>
        {(sortAscDesc)? 
        <p>Descending</p>:
        <p>Ascending</p>}
        </header>
        <Table players = {players}/>
      </>
    )
  
}

export default App
