import debitCard from "../images/asset-debit2.png";
import bkbox from "../images/asset-background.png";
import cryptoimg from "../images/asset-crypto2.png";
import bankimg from "../images/asset-bank2.png";

import AuthContext from '../context/AuthContext';
import { useContext } from "react";
import { useNavigate } from 'react-router-dom';

export default function LinkAssets() {
    //Retrieve the authentication tokens from the AuthContext component.
    let {authTokens, logoutUser} = useContext(AuthContext);
    //Used to handle navigation to the Plaid_link component once the link token is obtained.
    const navigate = useNavigate()

    //Function sends a GET request to the server with the product type as a parameter. The response is then parsed as JSON. 
    //If the response is successful (HTTP status code 200), the component navigates to the Plaid_link component with the link token as a state object.
    async function get_link_token(product) {
        let url = 'api/link_token?product=' + product
        let response = await fetch(url, {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        });
        let data = await response.json();
        if (response.status === 200) {
            navigate('/plaid_link', {
                state: {link_token: data['link_token']},
                replace: true
            });
        }

        
    }

    const buttClick = () => {
        let route = '/crypto_addresses';
        navigate(route);

    }

    let page1 = (<div>
        
        <div>
            <div className="assetLink_holder">
                <div className="background__box">
                <img className="background__image1" src={bkbox} alt="background__image1"></img>
                    <div className="asset__content">
                        <img className="debit__card__image" src={debitCard} alt="debit__card__image"></img>
                        <p className="debit-middle-text">Link your credit or debit card</p>
                        <button data-testid = 'linktransactions' className="link-button" onClick={async () => {await get_link_token("transactions");} }>Link</button>
                    </div>
                </div>
            </div>

        </div>
        <div>
            <div className="assetLink_holder">
                <div className="background__box">
                <img className="background__image2" src={bkbox} alt="background__image2"></img>
                    <div className="asset__content">
                        <img className="bank__image" src={bankimg} alt="bank__image"></img>
                        <p className="asset-middle-text">Link your brokerage account</p>
                        <button className="link-button" onClick={async () => {await get_link_token("investments");} }>Link</button>
                    </div>
                </div>
            </div>

        </div>
        <div>
            <div class="assetLink_holder">
                <div class="background__box">
                <img class="background__image3" src={bkbox} alt="background__image3"></img>
                    <div class="asset__content">
                        <img class="crypto__image" src={cryptoimg} alt="crypto__image"></img>
                        <p class="crypto-middle-text">Link your crypto wallet</p>
                        <button class="link-button" onClick={buttClick}>Link</button>
                    </div>
                </div>
            </div>

        </div>

     
    </div>
    )
    let page2 = (
        <div className='home-container flex flex-col my-10px mx-20 p-10 gap-8' data-testid="linkassetstest">
            <div className='link-debit flex flex-row justify-between gap-8 rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600 py-5 px-10'>
                <img className="debit_image ml-[-2rem]" src={debitCard} alt="debit_image"></img>
                <p className="middle-text text-center my-auto text-4xl text-white">Link your bank account</p>
                <button className="link-button rounded-[50px] text-lg py-2.5 px-10 border-2 my-auto text-center align-center text-lg" onClick={async () => {await get_link_token("transactions");} }>Link</button>
            </div>
            <div className='link-stocks flex flex-row justify-between gap-8 rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600 py-5 px-10'>
                <img className="stock_image" src={bankimg} alt="stock_image"></img>
                <p className="middle-text text-center my-auto text-4xl text-white">Link your brokerage account</p>
                <button className="link-button rounded-[50px] text-lg py-2.5 px-10 border-2 my-auto text-center align-center text-lg" onClick={async () => {await get_link_token("investments");} }>Link</button>
            </div>
            <div className='link-crypto flex flex-row justify-between gap-8 rounded-3xl shadow-lg bg-gradient-to-r from-violet-500 to-violet-600 py-5 px-10'>
                <img className="crypto_image" src={cryptoimg} alt="crypto_image"></img>
                <p className="middle-text text-center my-auto text-4xl text-white">Link your crypto wallet</p>
                <button className="link-button rounded-[50px] text-lg py-2.5 px-10 border-2 my-auto text-center align-center text-lg" onClick={async () => {await get_link_token("transactions");} }>Link</button>

            </div>
        </div>
    )
    
    return page2
}