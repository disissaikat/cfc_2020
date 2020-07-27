# cfc_2020
Call for Code Hackathon 2020 Code

Submission Name: Unified NGO Cross Platform App

Short Description:
Manage, track expenses and make payments for NGOs working towards relief work

Long Description:
Every year we are faced with multiple disasters around us which impact human lives and bring the necessity for relief groups to come forward in helping those in need. Many people who are not associated with any organizations also come forward in helping people by contributing to certain organizations of their choice. But the problem lies with the transparency of the process. An individual is not able to know how the funds are being utilized. Even for a relief organization it is difficult to know how much funds are being targeted by other organizations for a particular disaster. In the first scenario, lack of transparency can deter an individual from donating. While in the second scenario, mismanagement might creep up as multiple groups might be working to help people affected by one disaster, and there may be other victims who might not get enough funds or help.

This is where my idea fits in. An app for both individuals who want to contribute to a particular cause or for NGOs to track and manage expenses and plan relief work.

Individual – 
1.	Once an individual registers to the app using email an automated email denoting successful registration would be received. Then they can access all the NGOs registered on the platform. They can also view the disasters and the relief planned by them in order to extend their help accordingly. Suppose a group almost about to reach its target goal, is less likely to get a donation than a group that is yet to achieve its target amount by a long mile. An individual can then decide whom to donate to so that the funds are properly utilized. On successful payment a mail is sent to the user.
2.	An individual can also request to join a relief group in order to help people more closely and possibly spread out the word of the work being done for better exposure. Obviously his/her joining the group would be subject to approval from existing moderators of the relief groups. Once the request gets accepted or rejected, an email would be sent out as a notification to the user.
Organization – 
1.	An organization can register to the platform using its name, registration number provided by the government and suppose a short description as to where they are based and what kind of relief work, they do.
2.	Once registered, they can create activities as to where they want their work to be focused on, say ‘Floods in Assam’ or ‘Amphan Cyclone in West Bengal’ or ‘Earthquake in Nepal’. These data would not be some random disasters made up by organizations, but would be taken from API provided by https://reliefweb.int/ which is managed by ‘United Nations Office for the Coordination of Humanitarian Affairs’ so that fraud can be minimised and data integrity be maintained.
3.	During activity creation, a group would also be able to see how much amount has been planned for a particular disaster, so that they can better plan targets and scope of work.
4.	Once activities are created, members can contribute to the cause, add expenses for relief materials, track them and also view dashboards for contributors for donations as well as resources.
5.	Organization members would also have the ability to approve or reject group joining requests.
Other App Features –
1.	Users can view their individual transaction history.
2.	Users can also manage account information like updating email, password or profile picture or reset password using email.
Any existing solutions present in the market such as Google Play Store or Apple App Store, only help organizations to track expenses of their own. However, it does not give the bigger picture as to how other organizations are faring in current situation. This would help in bridging that gap. Also, the disasters would not be some random ones against which organizations would be collecting money. They would be centrally managed by the United Nations.

Solution Roadmap:
In today’s world where we are grappled by a pandemic, the solution could work seamlessly providing a bridge to gap the distancing norms between relief workers. Suppose in May 2020, 2 states in India, West Bengal and were devastated by super cyclone Amphan. During the pandemic it was really hard for relief workers to co-ordinate amongst themselves. An app like this would help them immensely and also people could contribute to such causes from the comfort of their homes.

Scope of Improvement –
1.	When an organization registers, it would provide its government certified registration number, which would be subject to validation by administrators using government webistes. This could also be automated using APIs provided by governments where that is feasible. This would result in genuine registrations instead of fake organizations and prevent money laundering and also would make organizations accountable for auditing purposes.
2.	Incorporate block chain technologies to track payments made to organizations and use that data to predict relief work being undertaken by groups who are not registered to the platform.

The app would require minimal funding if proper blockchain nodes are setup and processes automated, providing minimal human interaction and reducing costs. The only infrastructure required would be for databases to record transactions, that too could be reduced significantly with blockchain capabilities.

Since it is written on Python, the app would be seamlessly running on Windows, Mac, Unix, Android or iOS. It would not require separate code bases for every platform, but the single code base based on Python would do the trick. The app would be sustainable since there would be no frequent updates required and the solution would be helpful even years to come.

Services Used:
1.	IBM Cloud DB2
2.	IBM Cloud Object Storage Service
3.	Relief Web Disaster API - https://reliefweb.int/disasters
