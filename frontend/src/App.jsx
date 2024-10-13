import { useEffect, useState } from 'react'
import playerService from './services/forms'
import './App.css'

const Button = (props) => {
  const {text, onClick} = props
  return (
    <button className = " px-4 py-2 border-black border border-dashed hover:bg-gray-100" onClick = {onClick}>{text}</button>
  )
}

const Table = (props) => {
  const { players, sortAscDesc } = props;

  return (
      <table className="table-auto w-full border border-collapse">
        <thead className="bg-gray-200">
          <tr>
            <th className="px-4 py-2 text-left">rank</th>
            <th className="px-4 py-2 text-left">player</th>
            <th className="px-4 py-2 text-left">overall score</th>
            <th className="px-4 py-2 text-left">average fantasy points 2024</th>
            <th className="px-4 py-2 text-left">projected fantasy points 2025</th>
            <th className="px-4 py-2 text-left">consistency</th>
            <th className="px-4 py-2 text-left">injury risk</th>
            <th className="px-4 py-2 text-left">consistency and injury risk</th>
            <th className="px-4 py-2 text-left">position</th>
          </tr>
        </thead>
        {players?<tbody>
          {players.map((player, index) => (
            <tr key={index} className={`${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'} hover:bg-gray-100`}>
              <td className="px-4 py-2">{sortAscDesc ? index + 1 : players.length - index}</td>
              <td className="px-4 py-2">{player.player}</td>
              <td className="px-4 py-2">{player.overallScore}</td>
              <td className="px-4 py-2">{player.averageFPTS}</td>
              <td className="px-4 py-2">{player.projectedFPTS}</td>
              <td className="px-4 py-2">{player.consistency}</td>
              <td className="px-4 py-2">{player.injuryRisk}</td>
              <td className="px-4 py-2">{player.consistencyInjuryRisk}</td>
              <td className="px-4 py-2">{player.position}</td>
            </tr>
          ))}
        </tbody>:
        <tbody>
        <tr>
          <td className="px-4 py-2" colSpan="8">loading table...</td>
        </tr>
      </tbody>}
      </table>
    );
};

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
        <p className="text-4xl text-center"> fantasy projections rankings</p>
        <header>
          <p>sort by: </p>
          <div></div>
        <Button text = 'name' onClick = {() => handleClick(0)}></Button>
        <Button text = 'overall score' onClick = {() => handleClick(1)}></Button>
        <Button text = 'avg fantasy points' onClick = {() => handleClick(2)}></Button>
        <Button text = 'projected fantasy points' onClick = {() => handleClick(3)}></Button>
        <Button text = 'consistency' onClick = {() => handleClick(4)}></Button>
        <Button text = 'injury risk' onClick = {() => handleClick(5)}></Button>
        <Button text = 'c+ ir' onClick = {() => handleClick(6)}></Button>
        </header>
        <Table players = {players} sortAscDesc = {sortAscDesc}/>
      </>
    )
  
}

export default App
