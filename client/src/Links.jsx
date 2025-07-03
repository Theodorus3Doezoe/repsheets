import React, { useState, useEffect } from 'react'
import axios from 'axios';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css'; 


export default function Links() {

    const [links, setLinks] = useState([]);
    const [newLink, setNewLink] = useState("");



    function handleInputChange(event) {
        setNewLink(event.target.value);
    }

   function addLink(){
        if (newLink.trim() !== ""){
            const urlToAdd = newLink; // Sla de URL op voordat setNewLink wordt aangeroepen

            // 1. Voeg een placeholder-object toe aan de state
            // Dit object bevat de URL en een 'loading' status of placeholder voor de data
            const newLinkObject = { 
                id: Date.now(), 
                originalUrl: urlToAdd, 
                imageUrl: null, // Of een placeholder image URL
                price: null, 
                isLoading: true, // Nieuwe property om laadstatus bij te houden
                error: null // Nieuwe property voor foutafhandeling
            };

            setLinks(l => [...l, newLinkObject]);
            setNewLink(""); // Leeg het invoerveld direct

            axios.post("/scrape", { url: urlToAdd }) // Gebruik urlToAdd
                .then(response => {
                    console.log('API Data:', response.data);
                    const imageUrl = response.data.imageUrl;
                    const price = response.data.price;

                    // 2. Update het bestaande object in de state met de gescrapete data
                    setLinks(l => l.map(link => 
                        link.id === newLinkObject.id 
                            ? { ...link, imageUrl: imageUrl, price: price, isLoading: false }
                            : link
                    ));
                })
                .catch(error => {
                    console.error('Er is een fout opgetreden bij het scrapingen:', error);
                    // Update het object om de fout weer te geven
                    setLinks(l => l.map(link => 
                        link.id === newLinkObject.id 
                            ? { ...link, isLoading: false, error: 'Fout bij laden van data' }
                            : link
                    ));
                });
        }
    }

    function deleteLink(idToDelete) { // Pas de parameter aan naar 'id' i.p.v. 'index'
        const updatedLinks = links.filter(link => link.id !== idToDelete);
        setLinks(updatedLinks);
    }
    
  return (
    <div className="text-center w-screen h-screen">
      <div>
        <input 
          className="border-2 radius rounded-xs p-2.5"
          type="text" 
          placeholder='Enter a link'
          value={newLink}
          onChange={handleInputChange}
          />
          <button
            className="p-5 bg-green-500 hover:bg-green-400 rounded-md cursor-pointer text-3xl font-bold text-white transition duration-200"  
            onClick={addLink}
          >
            Add
          </button>
      </div>
        <ol className="text-3xl">
                {links.map((linkObject) => (
                    <li key={linkObject.id} className="mb-4 p-4 h-50 border rounded-md shadow-md flex items-center justify-evenly">
                        {/* Conditionele rendering op basis van isLoading en error */}
                        {linkObject.isLoading ? (
                            // Toon de Skeleton loaders terwijl de data laadt
                            // Pas de breedte en hoogte aan op basis van je verwachte content layout
                            <>
                                <Skeleton width={200} height={30} className="mb-2" /> {/* Voor de URL/Titel */}
                                <Skeleton circle={true} height={100} width={100} className="my-2" /> {/* Voor de afbeelding */}
                                <Skeleton width={120} height={30} className="mb-2" /> {/* Voor de prijs */}
                                <Skeleton width={80} height={40} /> {/* Voor de verwijderknop */}
                            </>
                        ) : linkObject.error ? (
                            // Toon een foutmelding als er een fout is opgetreden
                            <p className="text-red-500 text-xl font-semibold">Fout: {linkObject.error}</p>
                        ) : (
                            // Toon de daadwerkelijke data als het laden klaar is en er geen fout is
                            <>
                                <a 
                                    className="text-xl font-bold break-all mb-2 cursor-pointer text-blue-950"
                                    href={linkObject.originalUrl}
                                    target="_blank"                    
                                >{linkObject.originalUrl}</a>
                                
                                {linkObject.imageUrl && (
                                    <img 
                                        src={linkObject.imageUrl} 
                                        alt="Product" 
                                        className="h-50 object-contain my-2 border rounded-sm"
                                    />
                                )}
                                
                                {linkObject.price && (
                                    <span className="text-2xl font-semibold mb-2">Prijs: {linkObject.price}</span>
                                )}

                                <button 
                                    className="p-3 bg-red-500 hover:bg-red-400 rounded-md cursor-pointer font-bold text-white transition duration-200"  
                                    onClick={() => deleteLink(linkObject.id)}>Verwijder
                                </button>
                            </>
                        )}
                    </li>
                ))}
            </ol>
    </div>
  )
}
