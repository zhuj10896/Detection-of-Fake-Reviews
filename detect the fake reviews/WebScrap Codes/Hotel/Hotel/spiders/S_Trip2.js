const puppeteer = require('puppeteer');
const fs = require('fs-extra');
(async function main(){
	try{
		const browser = await puppeteer.launch({headless:true});
		const page = await browser.newPage();
		page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36');
		
		
		Urls=['https://www.tripadvisor.com/Hotel_Review-g60898-d1026630-Reviews-Mandarin_Oriental_Atlanta-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d111345-Reviews-Four_Seasons_Hotel_Atlanta-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d86260-Reviews-The_Ritz_Carlton_Atlanta-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d513075-Reviews-InterContinental_Buckhead_Atlanta-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d1556831-Reviews-Loews_Atlanta_Hotel-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d86286-Reviews-The_Whitley_A_Luxury_Collection_Hotel_Atlanta_Buckhead-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d673806-Reviews-The_Ellis_Hotel-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d1199584-Reviews-W_Atlanta_Downtown-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d5783572-Reviews-Hyatt_Regency_Atlanta_Perimeter_at_Villa_Christina-Atlanta_Georgia.html',
		'https://www.tripadvisor.com/Hotel_Review-g60898-d1231097-Reviews-The_St_Regis_Atlanta-Atlanta_Georgia.html'];
		//Urls=[]

		hotel_name=['Mandarin_Oriental','Four_Seasons','The_Ritz_Carlton','InterContinental_Buckhead','Loews',
		'The_Whitley','The_Ellis','W_Atlanta_Downtown','Hyatt_Regency Villa_Christina','St_Regis'];
	
		count_hotel=0;
		
		for(i of Urls){
		await page.goto(i);
		
		

		//await fs.writeFile(hotel_name[count_hotel]+'.txt','Name|Rating|Review|Review_Answer|Num_reviews|Num_likes\n');
		console.log(hotel_name[count_hotel]);
		

		stop=0;
		count_n=0;
		while(stop==0){
			await page.waitForSelector('div#REVIEWS');
			count_n++;
			console.log(count_n);
			//Create reviews to iterate
			
			if(await page.$('div.entry p span')!==null){
			const button = await page.$('div.entry p span');
			await button.click();
			await page.waitForSelector('div.prw_rup.prw_reviews_user_links_hsx span');
			//await page.waitForSelector('div.recommend-titleInline');
			}
			

			
			const reviews = await page.$$('div.review-container');
			await page.waitForSelector('div.review-container');
			var review_concat=[];
			for (review of reviews){
				const name = await review.$eval('div.info_text div',nam=>nam.innerText);
				const review_text = await review.$eval('p',nam=>nam.innerText);
				const rating_total = await review.$eval('div.ui_column.is-9 span',nam=>nam.getAttribute('class'));
				const rating = rating_total[rating_total.length-2];
				//console.log(await review.$('div.mgrRspnInline p'));
				
				var review_text_answer = "No answer given";
				var num_reviews = 0;
				var num_likes = 0;
				if(await review.$$eval('p',nam=>nam.length) > 1){
					review_text_answer = await review.$eval('div.mgrRspnInline p',nam=>nam.innerText);
				}
				//if(count_n==24){console.log(name)}
				//name!='816wyley' && name !='119lindsayh' && name!='hollio106' && name!='harto2017' && name!='nancybY3227UD' && name!='musajak' && name!='heathermN8074ET' && name!='A8448WCrobertm'
				if(await review.$$eval('span.ui_icon.thumbs-up-fill',nam=>nam.length)>1){
				//if(await review.$eval('div.memberBadgingNoText.is-shown-at-tablet span.ui_icon.pencil-paper',nam=>nam.innerText)!==null){
					num_reviews= await review.$eval('div.memberBadgingNoText.is-shown-at-tablet span:nth-child(2)',nam=>nam.innerText);
				//}

				if(await review.$$eval('div.memberBadgingNoText.is-shown-at-tablet span.badgetext',nam=>nam.length)>1){
					num_likes= await review.$eval('div.memberBadgingNoText.is-shown-at-tablet span:nth-child(4)',nam=>nam.innerText);
				}
				}

			review_concat.push({'Name':name, 'rating':rating,'Review_content':review_text.replace(/(\n)+/g,""),'Review_content_answer':review_text_answer.replace(/(\n)+/g,""),'Num_reviews':num_reviews,'Num_likes':num_likes});

				
			
			//await fs.appendFile(hotel_name[count_hotel]+'.txt',`"${name}"|"${rating}"|"${review_text.replace(/(\n)+/g,"")}"|"${review_text_answer.replace(/(\n)+/g,"")}"|"${num_reviews}"|"${num_likes}"\n`);
			
			
			}
			
			var url = 'mongodb://localhost:27017/Hotel_reviews';

			var MongoClient = require('mongodb').MongoClient;

			MongoClient.connect(url,function(err,client){
			//console.log('Connected succesfully');
			let db = client.db('Hotel_reviews')
			//console.log(num_reviews);
			//var review = {'Name':name, 'rating':rating,'Review_content':review_text.replace(/(\n)+/g,""),'Review_content_answer':review_text_answer.replace(/(\n)+/g,""),'Num_reviews':num_reviews,'Num_likes':num_likes};
			db.collection("users").insertMany(review_concat, function(err, res) {
        		if (err) throw err;
        		//console.log("Document inserted");
        		// close the connection to db when you are done with it
        	client.close();
    		});

			});


			//if(count_n==1){stop=1};
			
			const next_page = await page.$eval('a.nav.next.taLnk.ui_button.primary',nam=>nam.href);
			if(String(next_page)!==String(page.url())){
				await page.goto(String(next_page));
			}else{
				stop=1;
			};
		
		}
	count_hotel++;
	}




	await browser.close();
	}catch(e){
		console.log('Our error',e);
	}
})();