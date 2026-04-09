If agents could directly access each other's latent thoughts $Z$, communication would be maximally informative. But we can only observe agent states $H$. The identifiability question asks: is there a unique (up to trivial ambiguities like relabeling) mapping from $H$ back to $Z$?

**Without identifiability**: Any recovered "latent thoughts" could be arbitrary mixtures of the true thoughts. An autoencoder trained without appropriate constraints might learn a representation where "thought 1" is actually a blend of the true agent's mathematical reasoning, linguistic style, and confidence level — sharing this with another agent transmits garbled, uninterpretable information.

**With identifiability**: Recovered thoughts correspond (up to permutation and elementwise transformation) to true underlying factors. Each recovered dimension captures one genuine thought component. Sharing these between agents transmits semantically meaningful cognitive content that the receiver can productively integrate.

The practical consequence is direct: identifiability determines whether latent communication transmits **signal** or **noise**.
