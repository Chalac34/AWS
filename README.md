<h1><bold>TP AWS MANAGEMENT SSH KEY : </bold> </h1>
<h2>How to use</h2>
<h3>FLAG</h3>
<p>
  <ul>
    <li>-g --generate: generate a ssh key pair</li>
    <li>-i --instace: set a aws's instances id </li>
    <li>-k --key: set a ssh public key </li>
    <li>-d --distribute: add a ssh key in aws instance </li>
    <li>-r --revoke: delete a ssk key in aws instace </li>
    <li>-l -- list: list all ssh key of aws instance </li>
  </ul>
</p>
<h3>Command Exemple</h3>
<h4><bold><i>Generate a ssh key pair: </i></bold></h4>
<li>python manage.py -g/--generate</li>

<h4><bold><i>Distribute a ssh key pair: </i></bold></h4>
<li>python manage.py -d/--distribute -i/--instance [INSTANCE_ID] -k/--key [SSH_KEY </li>

<h4><bold><i>Delete a ssh key pair: </i></bold></h4>
<li>python manage.py -d/--delete -i/--instance [INSTANCE_ID] -k/--key [SSH_KEY]</li>

<h4><bold><i>List a ssh key pair: </i></bold></h4>
<li>python manage.py -l/--list -i/-instance [INSTANCE_ID]</li>

